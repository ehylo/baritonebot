import discord
from discord.ext import commands
from discord.commands import permissions, Option

from utils.const import GUILD_ID
from utils.embeds import slash_embed
from main import bot_db


class Embed(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(
            name='embed',
            description='send an embed to a channel',
            guild_ids=[GUILD_ID],
            default_permissions=False
        )
    @permissions.has_any_role(*sum((bot_db.mod_ids | bot_db.admin_ids).values(), []))
    async def embed(
        self,
        ctx,
        channel: Option(
            discord.TextChannel, name='channel', description='the channel to send the embed to', required=True
        ),
        title: Option(str, name='title', description='title for the embed'),
        description: Option(str, name='description', description='description for the embed'),
        color: Option(str, name='color', description='color for the embed'),
        image: Option(discord.Attachment, name='image', description='image for the embed'),
        field1: Option(str, name='field 1', description='separate title and description with ||'),
        field2: Option(str, name='field 2', description='separate title and description with ||'),
        field3: Option(str, name='field 3', description='separate title and description with ||'),
        field4: Option(str, name='field 4', description='separate title and description with ||'),
        field5: Option(str, name='field 5', description='separate title and description with ||'),
    ):
        title = '' if title is None else title
        description = '' if description is None else description
        if len(color) != 6:
            pass
        if color is not None:
            if len(color) != 6:
                return await slash_embed(
                    ctx, ctx.author, f'Hex codes are 6 char. long, yours is {len(color)} char. long, not 6'
                )
            color = int(str(color), 16)
        else:
            color = bot_db.embed_color[ctx.guild.id]
        embed_var = discord.Embed(color=color, title=title, description=description)
        if image is not None:
            if 'image/' not in image.type:
                return await slash_embed(ctx, ctx.author, 'That attachment is not an image', 'Not an Image')
            embed_var.set_image(url=image.url)
        for field in [field1, field2, field3, field4, field5]:
            if field is not None:
                embed_var.add_field(name=field.slit('||')[0], value=field.split('||')[1])
        await channel.send(embed=embed_var)
        await slash_embed(
            ctx, ctx.author, 'Sent the embed to ' + channel.mention, 'Sent', bot_db.embed_color[ctx.guild.id]
        )


def setup(bot):
    bot.add_cog(Embed(bot))
