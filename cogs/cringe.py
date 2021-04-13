import discord
import logging
import random
from discord.ext import commands
from cogs.help import Help
from cogs.const import mod_group, channel_embed, error_embed, helper_group, fault_footer, coolEmbedColor, timeDate

class Cringe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def cringe(self, ctx):
        num_lines = sum(1 for line in open("./data/cringe.txt"))
        cnum = (random.randint(1, num_lines)) - 1
        f = open("./data/cringe.txt", "r")
        urlImg = (f.readlines())[cnum]
        embedVar = discord.Embed(color = coolEmbedColor, timestamp=timeDate)
        embedVar.title = (':camera_with_flash:')
        embedVar.set_image(url=urlImg)
        embedVar.set_footer(text=(fault_footer))
        await ctx.send(embed=embedVar)

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
            f = open("./data/cringe.txt", "r")
            lines = f.readlines()
            res = [sub.replace('\n', '') for sub in lines]
            if url in res:
                with open("./data/cringe.txt", "r") as f:
                    lines = f.readlines()
                with open("./data/cringe.txt", "w") as f:
                    for line in lines:
                        if line.strip("\n") != url:
                            f.write(line)
                title = 'Removed'
                desc = ('I guess that wasn\'nt cringe enough')
                await channel_embed(ctx, title, desc)
                logging.info(f'{ctx.author.id} removed a cringe')
            else:
                desc = ('That url does not exist in the cringe db')
                await error_embed(ctx, desc)

    @cringe.command()
    @commands.check(helper_group)
    async def add(self, ctx, url=None):
        if len(ctx.message.attachments) == 0 and url == None:
            desc = ('You need to give a url or attachment to add cringe')
            await error_embed(ctx, desc)
        else:
            if ctx.message.attachments[0].url.lower().endswith(('.png', '.jpeg', '.jpg', '.gif')) or (url.startswith('https://') and url.endswith(('.png', '.jpeg', '.jpg', '.gif'))):
                f = open("./data/cringe.txt", "r")
                lines = f.readlines()
                res = [sub.replace('\n', '') for sub in lines]
                if len(ctx.message.attachments) > 0 or url not in res:
                    imgUrl = ctx.message.attachments[0].url
                    f = open("./data/cringe.txt", "a")
                    if len(ctx.message.attachments) > 0:
                        f.write(f'\n{imgUrl}')
                    else:
                        f.write(f'\n{url}')
                    f.close()
                    title = 'Added'
                    desc = 'Very cringe'
                    await channel_embed(ctx, title, desc)
                    logging.info(f'{ctx.author.id} added a cringe')
                else:
                    desc = 'That cringe already exists'
                    await error_embed(ctx, desc)
            else:
                desc = 'Invalid attachment, must be `.png`, `.gif`, `.jpeg`, or `.jpg` or an image url'
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
        if isinstance(error, commands.errors.CommandInvokeError):
            desc = (f'There is no cringe, please add one to use this command')
            await error_embed(ctx, desc)
        else:
            desc = None
            await error_embed(ctx, desc, error)
            logging.info(f'{ctx.author.id} tried to get help with the cringe command/use it but it gave the error: {error}')

def setup(bot):
    bot.add_cog(Cringe(bot))