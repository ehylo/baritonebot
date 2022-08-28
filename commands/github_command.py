import discord
from discord.ext import commands
from discord.commands import Option
from github import Github
from github.GithubException import UnknownObjectException

from main import bot_db
from utils.embeds import slash_embed
from utils.const import GUILD_ID, GITHUB_TOKEN


class GithubCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.github = Github(GITHUB_TOKEN)
        self.baritone_repo = self.github.get_repo('cabaletta/baritone')

    @discord.slash_command(
        name='github-info',
        description='shows information about the baritone repo',
        guild_ids=[GUILD_ID]
    )
    async def github_info(self, ctx):
        embed_var = discord.Embed(
            color=bot_db.embed_color[ctx.guild.id], title='Please wait while I gather the info'
        )
        interaction = await ctx.respond(embed=embed_var)
        message = await interaction.original_message()
        embed_var.title = 'cabaletta/baritone'
        embed_var.description = self.baritone_repo.description
        embed_var.url = 'https://github.com/cabaletta/baritone/'
        embed_var.add_field(name='Watchers', value=str(self.baritone_repo.subscribers_count))
        embed_var.add_field(name='Stars', value=str(self.baritone_repo.stargazers_count))
        embed_var.add_field(name='Forks', value=str(self.baritone_repo.forks_count))
        embed_var.add_field(name='Branches', value=str(self.baritone_repo.get_branches().totalCount))
        embed_var.add_field(name='Commits', value=str(self.baritone_repo.get_commits().totalCount))
        embed_var.add_field(
            name='Issues',
            value=f'{self.baritone_repo.open_issues_count} 🟢 | '
                  f'{self.baritone_repo.get_issues(state="closed").totalCount} 🔴'
        )
        embed_var.add_field(
            name='Pull Requests',
            value=f'{self.baritone_repo.get_pulls(state="open").totalCount} 🟢 | '
                  f'{self.baritone_repo.get_pulls(state="closed").totalCount} 🔴'
        )
        lang = self.baritone_repo.get_languages()
        total_bytes = 0
        lang_str = ''
        for i in lang.values():
            total_bytes += i
        for i in lang.keys():
            bts = lang[i]
            lang_str += f'{i}: {100 * round((bts / total_bytes), 4)}%, '
        embed_var.add_field(name='Languages', value=lang_str[:-2])
        embed_var.add_field(name='Releases', value=str(self.baritone_repo.get_releases().totalCount))
        embed_var.add_field(
            name='Latest Release',
            value=f'[{self.baritone_repo.get_latest_release().tag_name}]'
                  f'({self.baritone_repo.get_latest_release().html_url})'
        )
        embed_var.add_field(name='Created', value=f'<t:{int(self.baritone_repo.created_at.timestamp())}:F>')
        embed_var.set_thumbnail(url=self.github.get_organization('cabaletta').avatar_url)
        embed_var.set_footer(text=f'{ctx.author.name} | ID: {ctx.author.id}', icon_url=ctx.author.display_avatar.url)
        await message.edit(embed=embed_var)

    @discord.slash_command(name='github-search', description='search for pull requests or issues', guild_ids=[GUILD_ID])
    async def github_search(
        self,
        ctx,
        query: Option(name='query', description='your search string', required=True),
        state: Option(
            name='state',
            description='show open, closed, or both',
            choices=['Open', 'Closed', 'Both'],
            default='Both'
        ),
        search_type: Option(
            name='type',
            description='show issues, pull requests, or both',
            choices=['Issue', 'Pull Request', 'Both'],
            default='Both'
        )
    ):
        embed_var = discord.Embed(
            color=bot_db.embed_color[ctx.guild.id], title='Please wait while I gather the info'
        )
        interaction = await ctx.respond(embed=embed_var)
        message = await interaction.original_message()
        if state == 'Both':
            issues = self.github.search_issues(query=query, repo='cabaletta/baritone')
        else:
            issues = self.github.search_issues(query=query, repo='cabaletta/baritone', state=state.lower())
        description = ''
        total = 0
        for issue in issues:
            if 'pull' in issue.html_url and search_type == 'Issue' or \
                    'pull' not in issue.html_url and search_type == 'Pull Request':
                continue
            merge = False
            if 'pull' in issue.html_url and search_type != 'Issue':
                description += '<:pr:1007151714815705108>'
                data = self.baritone_repo.get_pull(number=issue.number)
                if data.state == 'closed':
                    if data.merged:
                        merge = True
            elif 'pull' not in issue.html_url and search_type != 'Pull Request':
                description += '<:issue:1007151394756755567>'
            description += f' [#{issue.number}]({issue.html_url}) '
            description += '🟣 ' if merge else '🔴 ' if issue.state == 'closed' else '🟢 '
            description += f'{issue.title}\n'
            total += 1
        title = str(total)
        title += ' open and closed ' if state == 'Both' else ' open ' if state == 'Open' else ' closed '
        title += 'pull request(s)' if search_type == 'Pull Request' \
            else 'issue(s)' if search_type == 'Issue' else 'issue(s) and pull request(s)'
        title += f' for 🔍`{query}`'
        embed_var.title = title
        embed_var.description = description[:4096]
        url = 'https://github.com/cabaletta/baritone/issues?q='
        url += 'is%3A' + state.lower() if state != 'Both' else ''
        url += '+is%3Aissue' if search_type == 'Issue' else '+is%3Apr' if search_type == 'Pull Request' else ''
        embed_var.url = f'{url}+{query.replace(" ", "+")}'
        embed_var.set_footer(text=f'{ctx.author.name} | ID: {ctx.author.id}', icon_url=ctx.author.display_avatar.url)
        await message.edit(embed=embed_var)
    """
    @discord.slash_command(
        name='github-issue',
        description='shows information about a specific issue',
        guild_ids=[GUILD_ID]
    )
    async def github_issue(
        self,
        ctx,
        issue_num: Option(int, name='number', description='issue number you want information on', required=True),
        # comment_num: Option(int, name='comment number', description='the comment number you want')
    ):
        try:
            data = self.baritone_repo.get_issue(number=issue_num)
        except UnknownObjectException:
            return
            #return await main.error_embed(ctx, 'That issue (or pull request) does not exist')
        if 'pull' in data.html_url:
            self.baritone_repo.get_pull(number=num)
            question = await main.channel_embed(ctx, 'Couldn\'t find that issue', 'But I did find a pull request with that nunber, would you like to see that instead?')
            await question.add_reaction('✅')

            def check(m):
                try:
                    return question.id == m.reference.message_id and m.author.id == ctx.author.id
                except AttributeError:
                    pass
            while True:
                try:
                    reaction = await self.bot.wait_for('reaction_add', timeout=3600, check=check)
                except asyncio.TimeoutError:
                    return await question.delete()
                else:
                    if str(reaction[0]) == '✅':
                        return self.pull(self, ctx, num, c_num)
        if c_num is None:
            labels = ''
            for i in data.labels:
                labels += f', {i.name}'
            labels = '(None)' if labels == '' else labels[2:]
            embed_var = discord.Embed(color=int(main.values(1), 16))
            embed_var.set_author(name=data.user.name, url=data.user.url, icon_url=f'https://github.com/{data.user.name}.png')
            embed_var.description(data.body)
            embed_var.url(data.url)
            state = '🔴' if data.state == 'closed' else '🟢'
            embed_var.title(f'#{data.number} {state} {data.title} ({data.comments})')
            embed_var.add_field(name='Created', value=f'<t:{int(data.created_at.timestamp())}:F>')
            embed_var.add_field(name='Last Updated', value=f'<t:{int(data.updated_at.timestamp())}:F>')
            embed_var.add_field(name='Labels', value=labels)
            embed_var.set_footer(text=f'{ctx.author.name} | ID: {ctx.author.id}', icon_url=ctx.author.avatar_url)
            return await ctx.send(embed=embed_var)
        else:
            if c_num.isDigit():
                print('get the specific comment')
            else:
                if c_num.lower() == 'all':
                    print('get a list of the comments')

    @discord.slash_command(
        name='github-pull-request',
        description='shows information about a specific pull request',
        guild_ids=[GUILD_ID]
    )
    async def github_pull(
        self,
        ctx,
        pull_num: Option(int, name='number', description='pull request number you want information on', required=True),
        comment_num: Option(int, name='comment number', description='the comment number you want')
    ):
        try:
            data = self.baritone_repo.get_pull(number=num)
        except UnknownObjectException:
            try:
                self.baritone_repo.get_issue(number=num)
                question = await main.channel_embed(ctx, 'Couldn\'t find that Pull', 'But I did find a issue with that nunber, would you like to see that instead?')
                await question.add_reaction('✅')

                def check(m):
                    try:
                        return question.id == m.reference.message_id and m.author.id == ctx.author.id
                    except AttributeError:
                        pass
                while True:
                    try:
                        reaction = await self.bot.wait_for('reaction_add', timeout=3600, check=check)
                    except asyncio.TimeoutError:
                        return await question.delete()
                    else:
                        if str(reaction[0]) == '✅':
                            return self.issue(self, ctx, num, c_num)

            except UnknownObjectException:
                return main.error_embed(ctx, 'That pull request (or issue) does not exist')
        if c_num is None:
            embed_var = discord.Embed(color=int(main.values(1), 16))
            embed_var.set_author(name=data.user.name, url=data.user.url, icon_url=f'https://github.com/{data.user.name}.png')
            embed_var.description(data.body)
            embed_var.url(data.url)
            state = '🟣' if data.merged else '🔴' if data.state == 'closed' else '🟢'
            embed_var.title(f'#{data.number} {state} {data.title} ({data.comments})')
            labels = ''
            for i in data.labels:
                labels += f', {i.name}'
            labels = '(None)' if labels == '' else labels[2:]
            embed_var.add_field(name='Created', value=f'<t:{int(data.created_at.timestamp())}:F>')
            embed_var.add_field(name='Last Updated', value=f'<t:{int(data.updated_at.timestamp())}:F>')
            embed_var.add_field(name='Labels', value=labels)
            embed_var.add_field(name='Diff', value=f'```diff\n+{data.additions} -{data.deletions}```')
            embed_var.set_footer(text=f'{ctx.author.name} | ID: {ctx.author.id}', icon_url=ctx.author.avatar_url)
            return await ctx.send(embed=embed_var)
        else:
            if c_num.isDigit():
                print('get the specific comment')
            else:
                if c_num.lower() == 'all':
                    print('get a list of the comments')
    """

def setup(bot):
    bot.add_cog(GithubCommand(bot))
