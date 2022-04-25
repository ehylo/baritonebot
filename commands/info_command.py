import discord
from discord.ext import commands
from discord.commands import Option

from utils.const import GUILD_ID


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name='user-info', description='shows information about a member/user', guild_ids=[GUILD_ID])
    async def user_info(
        self,
        ctx,
        user: Option(discord.User, name='user', description='the user to get information on', required=True)
    ):
        pass

    @discord.slash_command(name='server-info', description='shows information about the server', guild_ids=[GUILD_ID])
    async def server_info(self, ctx):
        pass


def setup(bot):
    bot.add_cog(Info(bot))
