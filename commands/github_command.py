import discord
from discord.ext import commands
from discord.commands import Option

from utils.const import GUILD_ID


class GithubCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(
        name='github-info',
        description='shows information about the baritone repo',
        guild_ids=[GUILD_ID]
    )
    async def github_info(self, ctx):
        pass

    @discord.slash_command(name='github-search', description='search for pull requests or issues', guild_ids=[GUILD_ID])
    async def github_search(
        self,
        ctx,
        query: Option(str, name='query', description='your search string', required=True),
        search_type: Option(str, name='type', description='issue or pull request', options=['Issue', 'Pull Request']),
        is_open: Option(bool, name='open', description='show open issues? set to false for only closed')
    ):
        pass

    @discord.slash_command(
        name='github-issue',
        description='shows information about a specific issue',
        guild_ids=[GUILD_ID]
    )
    async def github_issue(
        self,
        ctx,
        issue_num: Option(int, name='number', description='issue number you want information on', required=True),
        comment_num: Option(int, name='comment number', description='the comment number you want')
    ):
        pass

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
        pass


def setup(bot):
    bot.add_cog(GithubCommand(bot))
