from typing import Optional
import re
import logging

import discord
from discord.ext import commands

from utils import slash_embed

log = logging.getLogger('privileged.embed_command')


class Embed(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(description='send an embed to a channel')
    @discord.app_commands.default_permissions(ban_members=True)
    @discord.app_commands.describe(
        channel='the channel to send the embed to',
        title='title for the embed',
        description='description for the embed',
        color='color for the embed',
        image='image for the embed',
        field1='separate title and description with ||',
        field2='separate title and description with ||',
        field3='separate title and description with ||',
        field4='separate title and description with ||',
        field5='separate title and description with ||'
    )
    @discord.app_commands.rename(
        field1='field-1',
        field2='field-2',
        field3='field-3',
        field4='field-4',
        field5='field-5',
    )
    async def embed(
        self,
        inter: discord.Interaction,
        channel: discord.TextChannel,
        title: str = None,
        description: str = None,
        color: str = None,
        image: Optional[discord.Attachment] = None,
        field1: str = None,
        field2: str = None,
        field3: str = None,
        field4: str = None,
        field5: str = None,
    ):

        # make sure the title or description doesn't add a 'None' and instead adds an empty string
        title = '' if title is None else title
        description = '' if description is None else description

        # check if a color was given
        if color is not None:

            # make sure it is a valid hex color code
            if not re.search(r'^#[A-Fa-f\d]{6}|[A-Fa-f\d]{3}$', '#' + color):
                return await slash_embed(
                    inter,
                    inter.user,
                    r'That is not a valid hex-code, it **must** match this regex: `^#[A-Fa-f\d]{6}|[A-Fa-f\d]{3}$`'
                )

            # convert it to something discord can interpret
            color = int(str(color), 16)
        else:
            color = self.bot.db.get_embed_color(inter.guild.id)

        # start constructing the embed
        embed_var = discord.Embed(color=color, title=title, description=description)

        # check if an attachment was provided
        if image is not None:

            # make sure the attachment is an image
            if 'image/' not in image.content_type:
                return await slash_embed(inter, inter.user, 'That attachment is not an image', 'Not an Image')

            embed_var.set_image(url=image.url)

        # add the fields that were provided
        for field in [field1, field2, field3, field4, field5]:
            if field is not None:
                embed_var.add_field(name=field.split('||')[0], value=field.split('||')[1])

        await channel.send(embed=embed_var)
        await slash_embed(
            inter, inter.user, 'Sent the embed to ' + channel.mention, 'Sent', self.bot.db.get_embed_color(
                inter.guild.id
            )
        )
        log.info(f'{inter.user.id} sent and embed to {channel.id}')


async def setup(bot):
    await bot.add_cog(Embed(bot))
