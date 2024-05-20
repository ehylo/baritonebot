from typing import Literal
import logging

import discord
from discord.ext import commands
from github import Github
from github.GithubException import UnknownObjectException

from utils import slash_embed, GITHUB_TOKEN

log = logging.getLogger('commands.github_command')


class GithubCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.github = Github(GITHUB_TOKEN)
        self.baritone_repo = self.github.get_repo('cabaletta/baritone')

    @discord.app_commands.command(name='github-info', description='shows information about the baritone repo')
    async def github_info(self, inter: discord.Interaction):

        # we need to respond to the slash command as sometimes the GitHub api can take more than 10 seconds so this
        # ensures we can actually respond
        embed_var = discord.Embed(
            color=self.bot.db.get_embed_color(inter.guild.id), title='Please wait while I gather the information'
        )
        await inter.response.send_message(embed=embed_var)
        message = await inter.original_response()

        # start building the embed and add all the information
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

        # calculate the language percentages
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
        embed_var.set_footer(text=f'{inter.user.name} | ID: {inter.user.id}', icon_url=inter.user.display_avatar.url)

        # finally edit the original embed with all the gathered information
        await message.edit(embed=embed_var)

    @discord.app_commands.command(name='github-search', description='search for pull requests or issues')
    @discord.app_commands.describe(
        query='your search string',
        state='show open, closed, or both',
        search_type='show issues, pull requests, or both'
    )
    @discord.app_commands.rename(search_type='type')
    async def github_search(
        self,
        inter: discord.Interaction,
        query: str,
        state: Literal['Open', 'Closed', 'Both'] = 'Both',
        search_type: Literal['Issue', 'Pull Request', 'Both'] = 'Both'
    ):
        log.info(f'{inter.user.id} searched for {query} with state as {state} and type {search_type}')

        # we need to respond to the slash command as sometimes the GitHub api can take more than 10 seconds so this
        # ensures we can actually respond
        embed_var = discord.Embed(
            color=self.bot.db.get_embed_color(inter.guild.id), title='Please wait while I gather the information'
        )
        await inter.response.send_message(embed=embed_var)
        message = await inter.original_response()

        # get the search results from GitHub based on the users options, may take some time
        if state == 'Both':
            issues = self.github.search_issues(query=query, repo='cabaletta/baritone')
        else:
            issues = self.github.search_issues(query=query, repo='cabaletta/baritone', state=state.lower())

        # start building the embed I am going to send
        description = ''
        total = 0
        for issue in issues:
            # filter out the items we don't want
            if 'pull' in issue.html_url and search_type == 'Issue':
                continue
            if 'pull' not in issue.html_url and search_type == 'Pull Request':
                continue

            # add the pull request or issue emote to our description
            merge = False
            if 'pull' in issue.html_url and search_type != 'Issue':
                description += '<:pr:1241674718151577620>'  # '<:pr:1018604923849547979>'
                data = self.baritone_repo.get_pull(number=issue.number)
                if data.state == 'closed':
                    if data.merged:
                        merge = True
            elif 'pull' not in issue.html_url and search_type != 'Pull Request':
                description += '<:issue:1241674695347011594>'  # '<:issue:1018604945408278629>'

            # add the rest of the information (number, state, link, title, etc.)
            description += f' [#{issue.number}]({issue.html_url}) '
            description += '🟣 ' if merge else '🔴 ' if issue.state == 'closed' else '🟢 '
            description += f'{issue.title}\n'
            total += 1

        # build the rest of the embed
        title = str(total)
        title += ' open and closed ' if state == 'Both' else ' open ' if state == 'Open' else ' closed '
        if search_type == 'Pull Request':
            title += 'pull request(s)'
        elif search_type == 'Issue':
            title += 'issue(s)'
        else:
            title += 'issue(s) and pull request(s)'
        title += f' for 🔍`{query}`'

        embed_var.title = title
        embed_var.description = description[:4096]

        url = 'https://github.com/cabaletta/baritone/issues?q='
        url += 'is%3A' + state.lower() if state != 'Both' else ''
        url += '+is%3Aissue' if search_type == 'Issue' else '+is%3Apr' if search_type == 'Pull Request' else ''

        # finish it off and send it
        embed_var.url = f'{url}+{query.replace(" ", "+")}'
        embed_var.set_footer(text=f'{inter.user.name} | ID: {inter.user.id}', icon_url=inter.user.display_avatar.url)
        await message.edit(embed=embed_var)

    # TODO: fix the github-issue command and github-pull-request command
    # for now they will be commented out because of the horrible state they are both in
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
            question = await main.channel_embed(
                ctx,
                'Couldn\'t find that issue',
                'But I did find a pull request with that number, would you like to see that instead?'
            )
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
            embed_var.set_author(
                name=data.user.name, url=data.user.url, icon_url=f'https://github.com/{data.user.name}.png'
            )
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
                question = await main.channel_embed(
                    ctx,
                    'Couldn\'t find that Pull',
                    'But I did find a issue with that number, would you like to see that instead?'
                )
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
            embed_var.set_author(
                name=data.user.name, url=data.user.url, icon_url=f'https://github.com/{data.user.name}.png'
            )
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


async def setup(bot):
    await bot.add_cog(GithubCommand(bot))
