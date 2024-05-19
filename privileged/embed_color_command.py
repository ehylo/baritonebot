import re
import logging

import discord
from discord.ext import commands

from utils import slash_embed, DEFAULT_EMBED_COLOR

log = logging.getLogger('privileged.embed_color_command')


class EmbedColor(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name='embed-color', description='set the bot\'s embed color for this server')
    @discord.app_commands.default_permissions(ban_members=True)
    @discord.app_commands.describe(value='the color you want (Hex), or type "default" for the default color (81C3FF)')
    @discord.app_commands.rename(value='color')
    async def embed_color(self, inter: discord.Interaction, value: str):
        if value.lower() == 'default':
            value = DEFAULT_EMBED_COLOR
        if not re.search(r'^#[A-Fa-f\d]{6}|[A-Fa-f\d]{3}$', '#' + value):
            return await slash_embed(
                inter,
                inter.user,
                r'That is not a valid hex-code, it **must** match this regex: `^#[A-Fa-f\d]{6}|[A-Fa-f\d]{3}$`'
            )
        await self.bot.db.edit_embed_color(inter.guild.id, value)
        log.info(f'{inter.user.id} changed the embed color in {inter.guild.id} to {value}')
        return await slash_embed(
            inter,
            inter.user,
            f'Set the embed color of this server to {value}',
            'Embed-color set',
            self.bot.db.get_embed_color(inter.guild.id)
        )


async def setup(bot):
    await bot.add_cog(EmbedColor(bot))
