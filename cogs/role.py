import discord
import logging
from discord.ext import commands
from cogs.help import Help
from cogs.const import ignoreRole, releasesRole, channel_embed, error_embed

class Ignore(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def ignore(self, ctx):
        roleVar = discord.utils.get(ctx.guild.roles, id=ignoreRole)
        if roleVar in ctx.author.roles:
            desc = ('You already have the Ignored role!')
            await error_embed(ctx, desc)
        else:
            await ctx.author.add_roles(roleVar)
            title = (f'Ignored role obtained')
            desc = ('Your messages will not trigger most of the response regexes now.')
            await channel_embed(ctx, title, desc)
            logging.info(f'{ctx.author.id} gave themselfs ignore role')

    @ignore.command()
    async def help(self, ctx):
        await Help.ignore(self, ctx)

    @ignore.error
    @help.error
    async def role_error(self, ctx, error):
        desc = None
        await error_embed(ctx, desc, error)
        logging.info(f'{ctx.author.id} tried to remove ignore role but it gave the error: {error}')

class Unignore(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def unignore(self, ctx):
        roleVar = discord.utils.get(ctx.guild.roles, id=ignoreRole)
        if roleVar not in ctx.author.roles:
            desc = ("You don't have the Ignored role!")
            await error_embed(ctx, desc)
        else:
            await ctx.author.remove_roles(roleVar)
            title = (f'Ignored role lost')
            desc = ('Your messages will now trigger most of the response regexes.')
            await channel_embed(ctx, title, desc)
            logging.info(f'{ctx.author.id} removed ignore role')
        
    @unignore.command()
    async def help(self, ctx):
        await Help.ignore(self, ctx)

    @unignore.error
    @help.error
    async def role_error(self, ctx, error):
        desc = None
        await error_embed(ctx, desc, error)
        logging.info(f'{ctx.author.id} tried to remove ignore role but it gave the error: {error}')

class Releases(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def releases(self, ctx):
        roleVar = discord.utils.get(ctx.guild.roles, id=releasesRole)
        if roleVar in ctx.author.roles:
            desc = ('You already have the Releases role!')
            await error_embed(ctx, desc)
        else:
            await ctx.author.add_roles(roleVar)
            title = (f'Releases role obtained')
            desc = ('You will now be pinged when a new release is made!')
            await channel_embed(ctx, title, desc)
            logging.info(f'{ctx.author.id} gave themselfs releases role')

    @releases.command()
    async def help(self, ctx):
        await Help.releases(self, ctx)

    @releases.error
    @help.error
    async def role_error(self, ctx, error):
        desc = None
        await error_embed(ctx, desc, error)
        logging.info(f'{ctx.author.id} tried to add releases role but it gave the error: {error}')

class Unreleases(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def unreleases(self, ctx):
        roleVar = discord.utils.get(ctx.guild.roles, id=releasesRole)
        if roleVar not in ctx.author.roles:
            desc = ("You don't have the Releases role!")
            await error_embed(ctx, desc)
        else:
            await ctx.author.remove_roles(roleVar)
            title = (f'Releases role lost')
            desc = ('You now will not be pinged when a new release is made .')
            await channel_embed(ctx, title, desc)
            logging.info(f'{ctx.author.id} removed releases role')

    @unreleases.command()
    async def help(self, ctx):
        await Help.releases(self, ctx)

    @unreleases.error
    @help.error
    async def role_error(self, ctx, error):
        desc = None
        await error_embed(ctx, desc, error)
        logging.info(f'{ctx.author.id} tried to remove releases role but it gave the error: {error}')

def setup(bot):
    bot.add_cog(Ignore(bot))
    bot.add_cog(Unignore(bot))
    bot.add_cog(Releases(bot))
    bot.add_cog(Unreleases(bot))