import discord
from discord.commands import permissions, Option
from discord.ext import commands

from utils.const import GUILD_ID
from main import bot_db


class Prefix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(
        name='prefix',
        description='set the bot\'s prefix for this server',
        guild_ids=[GUILD_ID],
        default_permissions=False
    )
    @permissions.has_any_role(*sum(bot_db.admin_ids.values(), []))
    async def prefix(
        self,
        ctx,
        value: Option(
            str,
            name='prefix',
            description='the prefix you want (Hex), or type "default" for the default prefix (b?)',
            required=True
        )
    ):
        pass


def setup(bot):
    bot.add_cog(Prefix(bot))
