import discord
from discord.ext import commands

from utils.const import GUILD_ID


class MessageInteraction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.message_command(name='upload to paste.ee', guild_ids=[GUILD_ID])
    async def paste(self, ctx, message: discord.Message):
        pass

    @discord.message_command(name='raw contents', guild_ids=[GUILD_ID])
    async def raw_contents(self, ctx, message: discord.Message):
        pass

    @discord.message_command(name='embed json', guild_ids=[GUILD_ID])
    async def embed_json(self, ctx, message: discord.Message):
        pass

    @discord.message_command(name='user-info', guild_ids=[GUILD_ID])
    async def user_info(self, ctx, message: discord.Message):
        pass


def setup(bot):
    bot.add_cog(MessageInteraction(bot))
