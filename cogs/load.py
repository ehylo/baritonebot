import discord
import logging
from discord.ext import commands
from cogs.help import Help
from cogs.const import admin_group, channel_embed, error_embed

class Load(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.check(admin_group)
    async def load(self, ctx, extension=None):
        if extension == None:
            await Help.load(self, ctx)
        else:
            self.bot.load_extension(f'cogs.{extension}')
            title = ('Loaded Extension')
            desc = (f'The extension {extension} has been loaded')
            await channel_embed(ctx, title, desc)
            logging.info(f'{ctx.author.id} loaded the extension {extension}')

    @commands.command()
    @commands.check(admin_group)
    async def unload(self, ctx, extension=None):
        if extension == None:
            await Help.unload(self, ctx)
        else:
            self.bot.unload_extension(f'cogs.{extension}')
            desc = (f'The extension {extension} has been unloaded')
            title = ('Unloaded Extension')
            await channel_embed(ctx, title, desc)
            logging.info(f'{ctx.author.id} unloaded the extension {extension}')

    @commands.command()
    @commands.check(admin_group)
    async def reload(self, ctx, extension=None):
        if extension == None:
            await Help.reload(self, ctx)
        else:
            self.bot.unload_extension(f'cogs.{extension}')
            self.bot.load_extension(f'cogs.{extension}')
            desc = (f'The extension {extension} has been reloaded')
            title = ('Reloaded Extension')
            await channel_embed(ctx, title, desc)
            logging.info(f'{ctx.author.id} reloaded the extension {extension}')

    @load.error
    @unload.error
    @reload.error
    async def unreload_error(self, ctx, error):
        if isinstance(error, commands.errors.CheckFailure):
            desc = (f'You need to be an Admin to use the command `{ctx.command}`')
            await error_embed(ctx, desc)
        else:
            await error_embed(ctx, desc, error)
            logging.info(f'{ctx.author.id} tried to re/un/load {ctx.extension} but it gave the error: {error}')

def setup(bot):
    bot.add_cog(Load(bot))