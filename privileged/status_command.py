import discord
from discord.commands import Option
from discord.ext import commands

from utils import const
from utils.embeds import slash_embed
from main import bot_db


class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(
        name='status',
        description='set the bot\'s status',
        guild_ids=[const.GUILD_ID]
    )
    @discord.default_permissions(ban_members=True)
    async def status(
        self,
        ctx,
        action: Option(
            name='action',
            description='the action you want the bot todo',
            choices=['Watching', 'Playing', 'Listening to', 'Competing in'],
            required=True
        ),
        value: Option(
            name='status',
            description='the status you want, or type "default" for the default status ("humans interact")',
            required=True
        )
    ):
        if value.lower() == 'default':
            value = const.DEFAULT_PRESENCE_VALUE
        bot_db.update_presence_value(value)
        bot_db.update_presence_action(action)
        await self.bot.change_presence(
            activity=discord.Activity(
                type=const.PRESENCE_ACTION_KEY[bot_db.presence_action], name=bot_db.presence_value
            )
        )
        return await slash_embed(
            ctx,
            ctx.author,
            f'Set the status of the baritone bot to `{action} {value}`',
            'Status Set',
            bot_db.embed_color[ctx.guild.id]
        )


def setup(bot):
    bot.add_cog(Status(bot))
