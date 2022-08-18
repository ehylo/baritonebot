import re

import discord
from discord.commands import Option
from discord.ext import commands

from utils.embeds import slash_embed
from utils.const import GUILD_ID, DEFAULT_EMBED_COLOR
from main import bot_db


class EmbedColor(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(
        name='embed-color',
        description='set the bot\'s embed color for this server',
        guild_ids=[GUILD_ID]
    )
    @discord.default_permissions(ban_members=True)
    async def embed_color(
        self,
        ctx,
        value: Option(
            name='color',
            description='the color you want (Hex), or type "default" for the default color (81C3FF)',
            required=True
        )
    ):
        if value.lower() == 'default':
            value = DEFAULT_EMBED_COLOR
        if not re.search(r'^#[A-Fa-f\d]{6}|[A-Fa-f\d]{3}$', '#' + value):
            return await slash_embed(
                ctx,
                ctx.author,
                r'That is not a valid hex-code, it **must** match this regex: `^#[A-Fa-f\d]{6}|[A-Fa-f\d]{3}$`'
            )
        bot_db.update_embed_color(ctx.guild, value)
        return await slash_embed(
            ctx,
            ctx.author,
            f'Set the embed color of this server to {value}',
            'Embed-color set',
            bot_db.embed_color[ctx.guild.id]
        )


def setup(bot):
    bot.add_cog(EmbedColor(bot))
