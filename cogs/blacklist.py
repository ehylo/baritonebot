import discord
import logging
from discord.ext import commands
from cogs.help import Help
from cogs.const import helper_group, mod_group, error_embed, channel_embed, help_embed

class Blacklist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    @commands.check(helper_group)
    async def blacklist(self, ctx):
        await Help.blacklist(self, ctx)

    @blacklist.command()
    @commands.check(helper_group)
    async def list(self, ctx):
        #list the current blacklist
        title = ('Blacklisted Words')
        desc = ('(list of blacklisted words)')
        await channel_embed(ctx, title, desc)
    
    @blacklist.command()
    @commands.check(mod_group)
    async def add(self, ctx, word=None):
        if word == None:
            desc = ('You need to give a word to add')
            await error_embed(ctx, desc)
        else:
            #save 'word' to blacklist
            title = 'Added'
            desc = (f'The word `{word}` has been added to the blacklist')
            await channel_embed(ctx, title, desc)
            logging.info(f'{ctx.author.id} added a word to the blacklist')

    @blacklist.command()
    @commands.check(mod_group)
    async def remove(self, ctx, word=None):
        if word == None:
            desc = ('You need to give a word to remove')
            await error_embed(ctx, desc)
        else:
            try:
                #try to remove 'word'
                title = 'Removed'
                desc = (f'The word `{word}` has been removed from the blacklist')
                await channel_embed(ctx, title, desc)
                logging.info(f'{ctx.author.id} removed a word from the blacklist')
            except:
                desc = (f'`{word} isn\'t on the blacklist')
                await error_embed(ctx, desc)

    @list.error
    @blacklist.error
    async def listhelp_error(self, ctx, error):
        if isinstance(error, commands.errors.CheckFailure):
            desc = (f'You need to be a Helper to use the command `{ctx.command}`')
            await error_embed(ctx, desc)
        else:
            desc = None
            await error_embed(ctx, desc, error)
            logging.info(f'{ctx.author.id} tried to list the blacklisted words but it gave the error: {error}')

    @add.error
    @remove.error
    async def addremove_error(self, ctx, error):
        if isinstance(error, commands.errors.CheckFailure):
            desc = (f'You need to be a Moderator to use the command `{ctx.command}`')
            await error_embed(ctx, desc)
        else:
            desc = None
            await error_embed(ctx, desc, error)
            logging.info(f'{ctx.author.id} tried to add/remove word from blacklist but it gave the error: {error}')

def setup(bot):
    bot.add_cog(Blacklist(bot))