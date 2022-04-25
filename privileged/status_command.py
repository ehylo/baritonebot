import discord
from discord.commands import permissions, Option
from discord.ext import commands

from utils.const import GUILD_ID
from main import bot_db


class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(
        name='status',
        description='set the bot\'s status',
        guild_ids=[GUILD_ID],
        default_permissions=False
    )
    @permissions.has_any_role(*sum((bot_db.mod_ids | bot_db.admin_ids).values(), []))
    async def status(
        self,
        ctx,
        presence_type: Option(
            str,
            name='presence action',
            description='the action you want the bot todo',
            choices=['Watching', 'Playing', 'Listening to', 'Competing in'],
            required=True
        ),
        value: Option(
            str,
            name='status',
            description='the status you want, or type "default" for the default status ("humans interact")',
            required=True
        )
    ):
        pass


def setup(bot):
    bot.add_cog(Status(bot))
