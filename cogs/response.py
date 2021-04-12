import discord
import logging
from discord.ext import commands
from cogs.help import Help
from cogs.const import error_embed, help_embed, channel_embed, helper_group, mod_group

class Response(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    @commands.check(helper_group)
    async def response(self, ctx):
        await Help.response(self, ctx)

    @response.command()
    @commands.check(helper_group)
    async def list(self, ctx):
        #list the current responses
        title = 'Current Responses:'
        desc = ('*List of current responses*')
        await channel_embed(ctx, title, desc)

    @response.command()
    @commands.check(helper_group)
    async def details(self, ctx, rnum: int=None):
        if rnum == None:
            desc = 'You need to give the response number to get the details'
            await error_embed(ctx, desc)
        else:
            #might want to do if rnum is not in list[responses] instead of try and except
            try:
                #try to fetch response details
                title = f'Response #{rnum} details:'
                desc = ('*title, regex, and desc of response number*')
                await channel_embed(ctx, title, desc)
            except:
                desc = ('There is no response with that number yet')
                await error_embed(ctx, desc)

    @response.command()
    @commands.check(mod_group)
    async def remove(self, ctx, rnum: int=None):
        if rnum == None:
            desc = 'You need to give the response number to remove it'
            await error_embed(ctx, desc)
        else:
            #might want to do if rnum is not in list[responses] instead of try and except
            try:
                #try to remove it
                title = f'Removed response #{rnum}'
                desc = ('*title, regex, and desc of response removed*')
                await channel_embed(ctx, title, desc)
                logging.info(f'{ctx.author.id} removed response (maybe add number here)')
            except:
                desc = ('There is no response with that number')
                await error_embed(ctx, desc)

    @response.command()
    @commands.check(mod_group)
    async def add(self, ctx, etitle=None, regex=None, edesc=None):
        if etitle == None:
            desc = ('You need to give a title')
            await error_embed(ctx, desc)
        elif regex == None:
            desc = ('You need to give a regex')
            await error_embed(ctx, desc)
        elif edesc == None:
            desc = ('You need to give a description')
            await error_embed(ctx, desc)
        else:
            try:
                #is the regex valid (dont know if i can verify) then save given info as a new response
                title = 'New response:'
                desc = ('*title, regex, and desc of response added*')
                await channel_embed(ctx, title, desc)
                logging.info(f'{ctx.author.id} added response with title: {etitle}') #maybe add number here instead of title idk
            except:
                desc = ('The regex you gave is wrong')
                await error_embed(ctx, desc)

    @response.error
    @list.error
    @details.error
    async def listdetails_error(self, ctx, error):
        if isinstance(error, commands.errors.CheckFailure):
            desc = (f'You need to be a Helper to use the command `{ctx.command}`')
            await error_embed(ctx, desc)
        elif isinstance(error, commands.errors.BadArgument):
            desc = ('You need to give the response **number** to get the details')
            await error_embed(ctx, desc)                                         #FIND THIS ERROR TO CATCH
        else:
            desc = None
            await error_embed(ctx, desc, error)
            logging.info(f'{ctx.author.id} tried to add/remove word from blacklist but it gave the error: {error}')

    @add.error
    @remove.error
    async def addremove_error(self, ctx, error):
        if isinstance(error, commands.errors.CheckFailure):
            desc = (f'You need to be a Moderator to use the command `{ctx.command}`')
            await error_embed(ctx, desc)
        elif isinstance(error, commands.errors.BadArgument):
            desc = ('You need to give the response **number** to remove it')
            await error_embed(ctx, desc)                                         #FIND THIS ERROR TO CATCH
        else:
            desc = None
            await error_embed(ctx, desc, error)
            logging.info(f'{ctx.author.id} tried to add/remove word from blacklist but it gave the error: {error}')

def setup(bot):
    bot.add_cog(Response(bot))