import re

import discord
from discord.ext import commands
from discord.commands import Option

from utils.const import GUILD_ID
from utils.embeds import slash_embed
from main import bot_db


class Embed(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(
            name='embed',
            description='send an embed to a channel',
            guild_ids=[GUILD_ID]
        )
    @discord.default_permissions(ban_members=True)
    async def embed(
        self,
        ctx,
        channel: Option(
            discord.TextChannel, name='channel', description='the channel to send the embed to', required=True
        ),
        title: Option(name='title', description='title for the embed', required=False),
        description: Option(name='description', description='description for the embed', required=False),
        color: Option(name='color', description='color for the embed', required=False),
        image: Option(discord.Attachment, name='image', description='image for the embed', required=False),
        field1: Option(name='field-1', description='separate title and description with ||', required=False),
        field2: Option(name='field-2', description='separate title and description with ||', required=False),
        field3: Option(name='field-3', description='separate title and description with ||', required=False),
        field4: Option(name='field-4', description='separate title and description with ||', required=False),
        field5: Option(name='field-5', description='separate title and description with ||', required=False),
    ):
        title = '' if title is None else title
        description = '' if description is None else description
        if color is not None:
            if not re.search(r'^#[A-Fa-f\d]{6}|[A-Fa-f\d]{3}$', '#' + color):
                return await slash_embed(
                    ctx,
                    ctx.author,
                    r'That is not a valid hex-code, it **must** match this regex: `^#[A-Fa-f\d]{6}|[A-Fa-f\d]{3}$`'
                )
            color = int(str(color), 16)
        else:
            color = bot_db.embed_color[ctx.guild.id]
        embed_var = discord.Embed(color=color, title=title, description=description)
        if image is not None:
            if 'image/' not in image.content_type:
                return await slash_embed(ctx, ctx.author, 'That attachment is not an image', 'Not an Image')
            embed_var.set_image(url=image.url)
        for field in [field1, field2, field3, field4, field5]:
            if field is not None:
                embed_var.add_field(name=field.split('||')[0], value=field.split('||')[1])
        await channel.send(embed=embed_var)
        await slash_embed(
            ctx, ctx.author, 'Sent the embed to ' + channel.mention, 'Sent', bot_db.embed_color[ctx.guild.id]
        )


def setup(bot):
    bot.add_cog(Embed(bot))
