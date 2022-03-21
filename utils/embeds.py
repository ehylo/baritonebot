import discord

from utils.const import RED_EMBED_COLOR
from utils.misc import get_channel


async def dm_embed(bot_db, guild_id, channel: discord.TextChannel, author: discord.User, title: str, description: str):
    embed_var = discord.Embed(color=bot_db.embed_color[guild_id], title=title, description=description)
    embed_var.set_footer(text=f'{author.name} | ID: {author.id}', icon_url=author.avatar.url)
    await channel.send(embed=embed_var)


async def mod_log_embed(bot, bot_db, guild_id, author, offender, title, description):
    channel = await get_channel(bot, bot_db.mod_logs_id[guild_id])
    embed_var = discord.Embed(color=bot_db.embed_color[guild_id], title=title, description=description)
    embed_var.set_author(name=offender, icon_url=offender.avatar.url)
    embed_var.set_footer(text=f'{author.name} | ID: {author.id}', icon_url=author.avatar.url)
    await channel.send(embed=embed_var)


async def slash_embed(
    ctx: discord.ApplicationContext,
    author: discord.User,
    description: str = '',
    title: str = '',
    color: int = RED_EMBED_COLOR,
    ephemeral: bool = True,
    view: discord.ui.View = None,
    interaction: bool = False
):
    embed_var = discord.Embed(color=color, title=title, description=description)
    embed_var.set_footer(text=f'{author.name} | ID: {author.id}', icon_url=author.avatar.url)
    if interaction:
        await ctx.response.edit_message(embed=embed_var, view=view)
    else:
        await ctx.respond(embed=embed_var, ephemeral=ephemeral, view=view)
