import discord
import requests
import logging
from PIL import Image
from io import BytesIO
from discord.ext import commands
from cogs.help import Help
from cogs.const import mod_group, error_embed, channel_embed

class Emote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(invoke_without_command=True)
    @commands.check(mod_group)
    async def emote(self, ctx, name=None, url=None):
        if name == None:
            await Help.emote(self, ctx)
        elif len(ctx.message.attachments) > 0:
            if ctx.message.attachments[0].url.lower().endswith(('.png', '.jpeg', '.jpg', '.gif')):
                try:
                    imgUrl = ctx.message.attachments[0].url
                    icon = requests.get(imgUrl)
                    img = Image.open(BytesIO(icon.content), mode='r')
                    b = BytesIO()
                    img.save(b, format='PNG')
                    image = b.getvalue()
                    await ctx.guild.create_custom_emoji(name=name, image=image)
                    title = 'Created'
                    desc = (f'Emote `{name}` was created')
                    await channel_embed(ctx, title, desc)
                    logging.info(f'{ctx.author.id} created an emote')
                except:
                    desc = 'Emote cannot be larger than 256kb'
                    await error_embed(ctx, desc)
            else:
                desc = 'Invalid attachment, must be `.png` `.gif` `.jpeg` or `.jpg` or an image url'
                await error_embed(ctx, desc)
        elif url == None:
            desc = 'You need to either provide a link or attach a `.png` `.gif` `.jpeg` or `.jpg` to create an emote'
            await error_embed(ctx, desc)
        else:
            if url.endswith(('.png', '.jpeg', '.jpg', '.gif')):
                try:
                    icon = requests.get(url)
                    img = Image.open(BytesIO(icon.content), mode='r')
                    b = BytesIO()
                    img.save(b, format='PNG')
                    image = b.getvalue()
                    await ctx.guild.create_custom_emoji(name=name, image=image)
                    title = 'Created'
                    desc = (f'Emote `{name}` was created')
                    await channel_embed(ctx, title, desc)
                    logging.info(f'{ctx.author.id} created an emote')
                except:
                    desc = 'Emote cannot be larger than 256kb'
                    await error_embed(ctx, desc)
            else:
                desc = 'Url needs to end with `.png` `.gif` `.jpeg` or `.jpg`'
                await error_embed(ctx, desc)

    @emote.error
    async def emote_error(self, ctx, error):
        if isinstance(error, commands.errors.CheckFailure):
            desc = (f'You need to be a Moderator to use the command `{ctx.command}`')
            await error_embed(ctx, desc)
        else:
            desc = None
            await error_embed(ctx, desc, error)
            logging.info(f'{ctx.author.id} tried to add an emote but it gave the error: {error}')

def setup(bot):
    bot.add_cog(Emote(bot))