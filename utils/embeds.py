import discord

import utils


async def dm_embed(
    db, guild_id: int, channel: discord.DMChannel, author: discord.User, title: str, description: str
):
    embed_var = discord.Embed(color=db.embed_color[guild_id], title=title, description=description)
    embed_var.set_footer(text=f'{author.name} | ID: {author.id}', icon_url=author.display_avatar.url)
    await channel.send(embed=embed_var)


async def mod_log_embed(
    bot, db, guild_id: int, author: discord.Member, offender: discord.Member, title: str, description: str
):
    channel = await utils.misc.get_channel(bot, db.mod_logs_id[guild_id])
    embed_var = discord.Embed(color=db.embed_color[guild_id], title=title, description=description)
    embed_var.set_author(name=offender, icon_url=offender.display_avatar.url)
    embed_var.set_footer(text=f'{author.name} | ID: {author.id}', icon_url=author.display_avatar.url)
    await channel.send(embed=embed_var)


async def slash_embed(
    interaction: discord.Interaction,
    author: discord.User,
    description: str = '',
    title: str = '',
    color: int = utils.const.RED_EMBED_COLOR,
    ephemeral: bool = True,
    view: discord.ui.View = None,
    is_interaction: bool = False
):
    embed_var = discord.Embed(color=color, title=title, description=description)
    embed_var.set_footer(text=f'{author.name} | ID: {author.id}', icon_url=author.display_avatar.url)
    if is_interaction:
        await interaction.response.edit_message(embed=embed_var, view=view)
    else:
        if view is None:  # really shouldn't have to do this, but discord.py says otherwise
            return await interaction.response.send_message(embed=embed_var, ephemeral=ephemeral)
        await interaction.response.send_message(embed=embed_var, ephemeral=ephemeral, view=view)
