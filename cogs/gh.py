import asyncio
import main
import discord
from discord.ext import commands
from cogs.help import Help
from github import Github
from github.GithubException import UnknownObjectException

# - total merged is too slow as it makes a request for every pull (info) - could be fixed with the first todo

# TODO: When info command is used, grab information from db and then after, upload the new information
# TODO: Find out if I want to list the comments and have arrows for changing pages or just grab a specific comment
# TODO: Make sure the embed does not exceed limits (title for issues for example can be very long)
# TODO: Change all the nums in the info command to have links, find out if the name can have emebeded links in the text
# TODO: test the reaction for issue embed instead because I don't think it works

gh = Github(main.github_token)
brepo = gh.get_repo('cabaletta/baritone')


class Gh(commands.Cog):
    def __init__(self, bot):
        """Returns info from the GitHub api."""
        self.bot = bot

    @commands.group(invoke_without_command=True, case_insensitive=True, aliases=['gh'])
    async def github(self, ctx):
        return await Help.github(self, ctx)

    @github.command(aliases=['i'])
    async def info(self, ctx):
        em_v = discord.Embed(color=int(main.values(1), 16), title='\u200b', description='Please wait while I gather the information')
        message = await ctx.send(embed=em_v)
        em_v.title('cabaletta/baritone')
        em_v.description(brepo.description)
        em_v.url('https://github.com/cabaletta/baritone/')
        em_v.add_field(name='Watchers', value=str(brepo.watchers_count))
        em_v.add_field(name='Stars', value=str(brepo.stargazers_count))
        em_v.add_field(name='Forks', value=str(brepo.forks_count))
        em_v.add_field(name='Branches', value=str(brepo.get_branches().totalCount))
        em_v.add_field(name='Commits', value=str(brepo.get_commits().totalCount))
        em_v.add_field(name='Issues', value=f'{brepo.open_issues_count} 🟢 | {brepo.get_issues(state="closed").totalCount} 🔴')
        em_v.add_field(name='Pull Requests', value=f'{brepo.get_pulls(state="open").totalCount} 🟢 | {brepo.get_pulls(state="closed").totalCount} 🔴')
        lang = brepo.get_languages()
        total_bytes = 0
        lang_str = ''
        for i in lang.values():
            total_bytes += i
        for i in lang.keys():
            bts = lang[i]
            lang_str += f'{i}: {100 * round((bts / total_bytes), 4)}%, '
        em_v.add_field(name='Languages', value=lang_str[:-2])
        em_v.add_field(name='Releases', value=str(brepo.get_releases().totalCount))
        em_v.add_field(name='Latest Release', value=f'[{brepo.get_latest_release().tag_name}]({brepo.get_latest_release().html_url})')
        em_v.add_field(name='Created', value=f'<t:{int(brepo.created_at.timestamp())}:F>')
        em_v.set_thumbnail(url=gh.get_organization('cabaletta').avatar_url)
        em_v.set_footer(text=f'{ctx.author.name} | ID: {ctx.author.id}', icon_url=ctx.author.avatar_url)
        await message.edit(embed=em_v)

    @github.command(aliases=['s'])
    async def search(self, ctx, term=None, is_pull=None, is_open=None):
        if term is None:
            return await Help.github(self, ctx)
        if is_pull is None:
            return await main.error_embed(ctx, 'You need to say if you want to search for pull requests or issues')
        else:
            if is_pull.lower() in ['pull', 'pr', 'pullrequest']:
                is_pull = True
            elif is_pull.lower() == 'issue':
                is_pull = False
            else:
                return await main.error_embed(ctx, f'You need to provide either `issue` or `pull|pr|pullrequest` and not {is_pull}')
        if is_open is None:
            issues = gh.search_issues(query=term, repo='cabaletta/baritone')
            state = ''
        else:
            a_state = 'open' if is_open else 'closed'
            issues = gh.search_issues(query=term, repo='cabaletta/baritone', state=a_state)
            state = '+is%3Aopen' if is_open else '+is%3Aclosed'
        if is_pull:
            link = 'https://github.com/cabaletta/baritone/pull'
        else:
            link = 'https://github.com/cabaletta/baritone/issues'
        desc = ''
        for i in issues:
            mergee = False
            if is_pull and 'pull' in i.html_url:
                data = brepo.get_pull(number=i.number)
                if data.state == 'closed':
                    if data.merged:
                        mergee = True
                desc += 'PUT PULL EMOTE HERE'
            elif is_pull and 'pull' not in i.html_url or is_pull is False and 'pull' in i.html_url:
                continue
            elif not is_pull:
                desc += 'PUT ISSUE EMOTE HERE'
            desc += f' [#{i.number}]({link}/{i.number}) '
            desc += '🟣 ' if mergee else '🔴 ' if i.state == 'closed' else '🟢 '
            desc += f'{i.title}\n'
        title = 'All ' if is_open is None else 'Open ' if is_open else 'Closed '
        title += 'pull requests' if is_pull else 'issues'
        title += f' for `{term}` ({str(issues.totalCount)})'
        await main.channel_embed(ctx, title, desc, None, None, f'{link}?q={term.replace(" ", "+")}{state}')

    @commands.command(aliases=['i'])
    async def issue(self, ctx, num: int = None, c_num=None):
        if num is None:
            return await Help.issue(self, ctx)
        try:
            data = brepo.get_issue(number=num)
        except UnknownObjectException:
            return await main.error_embed(ctx, 'That issue (or pull request) does not exist')
        if 'pull' in data.html_url:
            brepo.get_pull(number=num)
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
            em_v = discord.Embed(color=int(main.values(1), 16))
            em_v.set_author(name=data.user.name, url=data.user.url, icon_url=f'https://github.com/{data.user.name}.png')
            em_v.description(data.body)
            em_v.url(data.url)
            state = '🔴' if data.state == 'closed' else '🟢'
            em_v.title(f'#{data.number} {state} {data.title} ({data.comments})')
            em_v.add_field(name='Created', value=f'<t:{int(data.created_at.timestamp())}:F>')
            em_v.add_field(name='Last Updated', value=f'<t:{int(data.updated_at.timestamp())}:F>')
            em_v.add_field(name='Labels', value=labels)
            em_v.set_footer(text=f'{ctx.author.name} | ID: {ctx.author.id}', icon_url=ctx.author.avatar_url)
            return await ctx.send(embed=em_v)
        else:
            if c_num.isDigit():
                print('get the specific comment')
            else:
                if c_num.lower() == 'all':
                    print('get a list of the comments')

    @commands.command(aliases=['pr'])
    async def pull(self, ctx, num: int = None, c_num=None):
        if num is None:
            return await Help.pull(self, ctx)
        try:
            data = brepo.get_pull(number=num)
        except UnknownObjectException:
            try:
                brepo.get_issue(number=num)
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
            em_v = discord.Embed(color=int(main.values(1), 16))
            em_v.set_author(name=data.user.name, url=data.user.url, icon_url=f'https://github.com/{data.user.name}.png')
            em_v.description(data.body)
            em_v.url(data.url)
            state = '🟣' if data.merged else '🔴' if data.state == 'closed' else '🟢'
            em_v.title(f'#{data.number} {state} {data.title} ({data.comments})')
            labels = ''
            for i in data.labels:
                labels += f', {i.name}'
            labels = '(None)' if labels == '' else labels[2:]
            em_v.add_field(name='Created', value=f'<t:{int(data.created_at.timestamp())}:F>')
            em_v.add_field(name='Last Updated', value=f'<t:{int(data.updated_at.timestamp())}:F>')
            em_v.add_field(name='Labels', value=labels)
            em_v.add_field(name='Diff', value=f'```diff\n+{data.additions} -{data.deletions}```')
            em_v.set_footer(text=f'{ctx.author.name} | ID: {ctx.author.id}', icon_url=ctx.author.avatar_url)
            return await ctx.send(embed=em_v)
        else:
            if c_num.isDigit():
                print('get the specific comment')
            else:
                if c_num.lower() == 'all':
                    print('get a list of the comments')


def setup(bot):
    bot.add_cog(Gh(bot))
