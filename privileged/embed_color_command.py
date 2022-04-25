import discord
from discord.commands import permissions, Option
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
        guild_ids=[GUILD_ID],
        default_permissions=False
    )
    @permissions.has_any_role(*sum((bot_db.mod_ids | bot_db.admin_ids).values(), []))
    async def embed_color(
        self,
        ctx,
        value: Option(
            str,
            name='color',
            description='the color you want (Hex), or type "default" for the default color (81C3FF)',
            required=True
        )
    ):
        if value.lower() == 'default':
            bot_db.update_embed_color(ctx.guild.id, DEFAULT_EMBED_COLOR)
            return await slash_embed(
                ctx,
                ctx.author,
                f'Set the embed color of this server to the default ({DEFAULT_EMBED_COLOR})',
                'Embed-color set',
                bot_db.embed_color[ctx.guild.id]
            )
        if len(value) != 6:
            return await slash_embed(ctx, ctx.author, f'Hex codes are 6 char. long, yours is {len(value)} char. long')
        bot_db.update_embed_color(ctx.guild.id, value)
        return await slash_embed(
            ctx,
            ctx.author,
            f'Set the embed color of this server to {value}',
            'Embed-color set',
            bot_db.embed_color[ctx.guild.id]
        )


def setup(bot):
    bot.add_cog(EmbedColor(bot))
