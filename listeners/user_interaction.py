import discord
from discord.ext import commands

from utils.const import GUILD_ID


class UserInteraction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.user_command(name='user-info', guild_ids=[GUILD_ID])
    async def user_info(self, ctx, member: discord.Member):
        pass

    @discord.user_command(name='user-avatar', guild_ids=[GUILD_ID])
    async def user_avatar(self, ctx, member: discord.Member):
        pass

    @discord.user_command(name='user-banner', guild_ids=[GUILD_ID])
    async def user_banner(self, ctx, member: discord.Member):
        pass


def setup(bot):
    bot.add_cog(UserInteraction(bot))
