import discord
import logging
from discord.ext import commands
from cogs.help import Help
from cogs.const import mod_group, channel_embed, error_embed, help_embed, helper_group

class Cringe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def cringe(self, ctx):
        #grab a random cringe and send it
        title = (':camera_with_flash:')
        desc = None
        await channel_embed(ctx, title, desc)

    @cringe.command()
    async def help(self, ctx):
        await Help.cringe(self, ctx)

    @cringe.command()
    @commands.check(mod_group)
    async def remove(self, ctx, url=None):
        if url == None:
            desc = ('You need to give a url to remove')
            await error_embed(ctx, desc)
        else:
            try:
                #search to see if url exist in cringe json, if it does remove
                title = 'Removed'
                desc = ('I guess that wasn\'nt cringe enough')
                await channel_embed(ctx, title, desc)
                logging.info(f'{ctx.author.id} removed a cringe')
            except:
                desc = ('That url does not exist in the cringe db')
                await error_embed(ctx, desc)

    @cringe.command()
    @commands.check(helper_group)
    async def add(self, ctx, url=None):
        if len(ctx.message.attachments) > 0:
            if ctx.message.attachments[0].url.lower().endswith(('.png', '.jpeg', '.jpg', '.gif')):
                imgUrl = ctx.message.attachments[0].url
                #add url to cringe
                title = 'Added'
                desc = ('Very cringe')
                await channel_embed(ctx, title, desc)
                logging.info(f'{ctx.author.id} added a cringe')
            else:
                desc = 'Invalid attachment, must be `.png` `.gif` `.jpeg` or `.jpg` or an image url'
                await error_embed(ctx, desc)
        elif url == None:
            desc = ('You need to give a url or attachment to add cringe')
            await error_embed(ctx, desc)
        else:
            try:
                #check if url is an image, if it is add
                title = 'Added'
                desc = 'Very cringe'
                await channel_embed(ctx, title, desc)
                logging.info(f'{ctx.author.id} added a cringe')
            except:
                desc = 'That url is not an image'
                await error_embed(ctx, desc)
    
    @remove.error
    async def remove_error(self, ctx, error):
        if isinstance(error, commands.errors.CheckFailure):
            desc = (f'You need to be a Moderator to use the command `{ctx.command}`')
            await error_embed(ctx, desc)
        else:
            desc = None
            await error_embed(ctx, desc, error)
            logging.info(f'{ctx.author.id} tried to remove a cringe but it gave the error: {error}')

    @add.error
    async def add_error(self, ctx, error):
        if isinstance(error, commands.errors.CheckFailure):
            desc = (f'You need to be a Helper to use the command `{ctx.command}`')
            await error_embed(ctx, desc)
        else:
            desc = None
            await error_embed(ctx, desc, error)
            logging.info(f'{ctx.author.id} tried to add a cringe but it gave the error: {error}')

    @cringe.error
    @help.error
    async def help_error(self, ctx, error):
        desc = None
        await error_embed(ctx, desc, error)
        logging.info(f'{ctx.author.id} tried to get help with the cringe command/use it but it gave the error: {error}')

def setup(bot):
    bot.add_cog(Cringe(bot))