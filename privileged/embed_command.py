import discord
from discord.ext import commands
from discord.commands import permissions, Option

from utils.const import GUILD_ID
from main import bot_db


class Embed(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(
            name='embed',
            description='send an embed to a channel',
            guild_ids=[GUILD_ID],
            default_permissions=False
        )
    @permissions.has_any_role(*sum((bot_db.mod_ids | bot_db.admin_ids).values(), []))
    async def embed(
        self,
        ctx,
        channel: Option(
            discord.TextChannel, name='channel', description='the channel to send the embed to', required=True
        ),
        title: Option(str, name='title', description='title for the embed'),
        description: Option(str, name='description', description='description for the embed'),
        color: Option(str, name='color', description='color for the embed'),
        image: Option(str, name='image', description='image for the embed'),
        field1: Option(str, name='field 1', description='separate title and description with ||'),
        field2: Option(str, name='field 2', description='separate title and description with ||'),
        field3: Option(str, name='field 3', description='separate title and description with ||'),
        field4: Option(str, name='field 4', description='separate title and description with ||'),
        field5: Option(str, name='field 5', description='separate title and description with ||'),
    ):
        pass


def setup(bot):
    bot.add_cog(Embed(bot))
