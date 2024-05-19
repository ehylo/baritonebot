from typing import Literal

import discord
from discord.ext import commands

from utils import slash_embed, DEFAULT_PRESENCE_VALUE, PRESENCE_ACTION_KEY


class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(description='set the bot\'s status')
    @discord.app_commands.describe(
        action='the action you want the bot todo',
        value='the status you want, or type "default" for the default status ("humans interact")'
    )
    @discord.app_commands.rename(value='status')
    @discord.app_commands.default_permissions(ban_members=True)
    async def status(
        self,
        inter: discord.Interaction,
        action: Literal['Watching', 'Playing', 'Listening to', 'Competing in'],
        value: str
    ):
        if value.lower() == 'default':
            value = DEFAULT_PRESENCE_VALUE
        await self.bot.db.edit_presence_value(value)
        await self.bot.db.edit_presence_action(action)
        await self.bot.change_presence(
            activity=discord.Activity(
                type=PRESENCE_ACTION_KEY[self.bot.db.presence_action], name=self.bot.db.presence_value
            )
        )
        return await slash_embed(
            inter,
            inter.user,
            f'Set the status of the baritone bot to `{action} {value}`',
            'Status Set',
            self.bot.db.get_embed_color(inter.guild.id)
        )


async def setup(bot):
    await bot.add_cog(Status(bot))
