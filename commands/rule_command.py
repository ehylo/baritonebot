# TODO complete rule command and parameters

import discord
from discord.ext import commands

from utils.const import GUILD_ID


class Rule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name='rule', description='show a specific rule', guild_ids=[GUILD_ID])
    async def rule(self, ctx):
        pass


def setup(bot):
    bot.add_cog(Rule(bot))
