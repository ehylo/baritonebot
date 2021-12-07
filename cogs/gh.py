import main
import discord
from discord.ext import commands
from cogs.help import Help
from github import Github
from github.GithubException import UnknownObjectException

'''
b?github <[search]|[info]> <[word]> <issue/pull> <open/closed>
(for search)
- total merged is too slow as it makes a request for every pull (info)
b?issue <[number]> <[comments]>
b?pull <[number]> <[comments]>
'''

gh = Github(main.github_token)
brepo = gh.get_repo('cabaletta/baritone')


class Gh(commands.Cog):
    def __init__(self, bot):
        """Returns info from the GitHub api"""
        self.bot = bot

    @commands.group(invoke_without_command=True, case_insensitive=True, aliases=['gh'])
    async def github(self, ctx):
        return await Help.github(self, ctx)

    @github.command(aliases=['i'])
    async def info(self, ctx):
        em_v = discord.Embed(color=int(main.values(1), 16), title='\u200b', description='Please wait while I gather the information')
        message = await ctx.send(embed=em_v)
        em_v = discord.Embed(color=int(main.values(1), 16), title='cabaletta/baritone', description=brepo.description, url='https://github.com/cabaletta/baritone/')
        em_v.add_field(name='Watchers', value=str(brepo.watchers_count), inline=True)
        em_v.add_field(name='Stars', value=str(brepo.stargazers_count), inline=True)
        em_v.add_field(name='Forks', value=str(brepo.forks_count), inline=True)
        em_v.add_field(name='Branches', value=str(brepo.get_branches().totalCount), inline=True)
        em_v.add_field(name='Commits', value=str(brepo.get_commits().totalCount), inline=True)
        em_v.add_field(name='Issues', value=f'{brepo.open_issues_count} 🟢 | {brepo.get_issues(state="closed").totalCount} 🔴', inline=True)
        em_v.add_field(name='Pull Requests', value=f'{brepo.get_pulls(state="open").totalCount} 🟢 | {brepo.get_pulls(state="closed").totalCount} 🔴', inline=True)
        lang = brepo.get_languages()
        total_bytes = 0
        lang_str = ''
        for i in lang.values():
            total_bytes += i
        for i in lang.keys():
            bts = lang[i]
            lang_str += f'{i}: {100 * round((bts / total_bytes), 4)}%, '
        em_v.add_field(name='Languages', value=lang_str[:-2], inline=True)
        em_v.add_field(name='Releases', value=str(brepo.get_releases().totalCount), inline=True)
        em_v.add_field(name='Latest Release', value=brepo.get_latest_release().html_url, inline=True)
        em_v.add_field(name='Created', value=f'<t:{int(brepo.created_at.timestamp())}:F>', inline=True)
        em_v.set_thumbnail(url=gh.get_organization('cabaletta').avatar_url)
        em_v.set_footer(text=f'{ctx.author.name} | ID: {ctx.author.id}', icon_url=ctx.author.avatar_url)
        await message.edit(embed=em_v)

    @github.command(aliases=['s'])
    async def search(self, ctx, *, term, is_pull, is_open=None):
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
            elif is_pull is False:
                desc += 'PUT ISSUE EMOTE HERE'
            desc += f' [#{i.number}]({link}/{i.number}) '
            desc += '🟣 ' if mergee else '🔴 ' if i.state == 'closed' else '🟢 '
            desc += f'{i.title}\n'
        title = 'All ' if is_open is None else 'Open ' if is_open else 'Closed '
        title += 'pull requests' if is_pull else 'issues'
        title += f' for `{term}` ({str(issues.totalCount)})'
        await main.channel_embed(ctx, title, desc, None, None, f'{link}?q={term.replace(" ", "+")}{state}')

    @commands.command(aliases=['i'])
    async def issue(self, ctx, num, c_num=None):
        data = brepo.get_issue(number=num)
        if 'pull' in data.html_url:
            return print('that is a pull')
        if c_num is None:
            desc = data.body
            title = data.title
            url = data.url
            comment_num = data.comments
            create_date = data.created_at
            labels = ''
            for i in data.labels:
                labels += f', {i.name}'
            labels = '(None)' if labels == '' else labels[2:]
            updated = data.updated_at
            create_user = data.user.name
            user_url = data.user.url
            state = data.state
            print('issue embed')
        else:
            print('comment')
        print('issue')

    @commands.command(aliases=['pr'])
    async def pull(self, ctx, num, c_num=None):
        try:
            data = brepo.get_pull(number=num)
        except UnknownObjectException:
            return print('not a pull')
        if c_num is None:
            desc = data.body
            title = data.title
            url = data.url
            comment_num = data.comments
            create_date = data.created_at
            labels = ''
            for i in data.labels:
                labels += f', {i.name}'
            labels = labels[2:]
            updated = data.updated_at
            create_user = data.user.name
            user_url = data.user.url
            state = 'merged' if data.merged else data.state
            diff_num = f'+{data.additions} -{data.deletions}'
            print('send pull info embed')
        else:
            print('comment stuff')
        print('pull')


def setup(bot):
    bot.add_cog(Gh(bot))
