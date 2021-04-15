import requests
import logging
import discord
from PIL import Image
from io import BytesIO
from discord.ext import commands
from cogs.help import Help
from cogs.const import mod_group, error_embed, channel_embed


async def create_emote(ctx, name, img_url):
    try:
        icon = requests.get(img_url)
        img = Image.open(BytesIO(icon.content), mode='r')
        b = BytesIO()
        img.save(b, format='PNG')
        image = b.getvalue()
        await ctx.guild.create_custom_emoji(name=name, image=image)
        await channel_embed(ctx, 'Created', f'Emote `{name}` was created')
        logging.info(f'{ctx.author.id} created an emote')
    except discord.HTTPException:
        await error_embed(ctx, 'Emote cannot be larger than 256kb')


class Emote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(invoke_without_command=True)
    @commands.check(mod_group)
    async def emote(self, ctx, name=None, url=None):
        if name is None:
            await Help.emote(self, ctx)
        elif len(ctx.message.attachments) > 0:
            if ctx.message.attachments[0].url.lower().endswith(('.png', '.jpeg', '.jpg', '.gif')):
                await create_emote(ctx, name, ctx.message.attachments[0].url)
            else:
                await error_embed(ctx, 'Invalid attachment, must be `.png` `.gif` `.jpeg` or `.jpg` or an image url')
        elif url is None:
            await error_embed(ctx, 'You need to either provide a link or attach a `.png` `.gif` `.jpeg` or `.jpg` to create an emote')
        else:
            if url.endswith(('.png', '.jpeg', '.jpg', '.gif')):
                await create_emote(ctx, name, url)
            else:
                await error_embed(ctx, 'Url needs to end with `.png` `.gif` `.jpeg` or `.jpg`')


def setup(bot):
    bot.add_cog(Emote(bot))
