import discord

from utils import get_channel, RED_EMBED_COLOR


async def dm_embed(
    db, guild_id: int, channel: discord.DMChannel, author: discord.User, title: str, description: str
):
    embed_var = discord.Embed(color=db.get_embed_color(guild_id), title=title, description=description)
    embed_var.set_footer(text=f'{author.name} | ID: {author.id}', icon_url=author.display_avatar.url)
    await channel.send(embed=embed_var)


async def mod_log_embed(
    bot, db, guild_id: int, author: discord.Member, offender: discord.Member, title: str, description: str
):
    channel = await get_channel(bot, db.get_mod_logs_channel_id(guild_id))
    embed_var = discord.Embed(color=db.get_embed_color(guild_id), title=title, description=description)
    embed_var.set_author(name=offender, icon_url=offender.display_avatar.url)
    embed_var.set_footer(text=f'{author.name} | ID: {author.id}', icon_url=author.display_avatar.url)
    await channel.send(embed=embed_var)


async def slash_embed(
    interaction: discord.Interaction,
    author: discord.User,
    description: str = '',
    title: str = '',
    color: int = RED_EMBED_COLOR,
    ephemeral: bool = True,
    view: discord.ui.View = None,
    is_interaction: bool = False
):

    # make sure the title is in the correct bounds
    if len(title) > 255:
        title = title[:250] + '...'

    # make sure the description is in the correct bounds
    if len(description) > 4095:
        description = description[:4090] + '...'

    embed_var = discord.Embed(color=color, title=title, description=description)
    embed_var.set_footer(text=f'{author.name} | ID: {author.id}', icon_url=author.display_avatar.url)

    # if it is an interaction we want to edit the response
    if is_interaction:
        await interaction.response.edit_message(embed=embed_var, view=view)

    # otherwise just respond to the message
    else:

        # view cannot be None, so we have to add this check
        if view is None:  # really shouldn't have to do this, but discord.py says otherwise
            return await interaction.response.send_message(embed=embed_var, ephemeral=ephemeral)

        await interaction.response.send_message(embed=embed_var, ephemeral=ephemeral, view=view)
