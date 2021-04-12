import discord
import logging
from discord.ext import commands
from cogs.help import Help
from cogs.const import ignoreRole, releasesRole, channel_embed, error_embed

class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ignore(self, ctx, elp=None):
        roleVar = discord.utils.get(ctx.guild.roles, id=ignoreRole)
        if elp == 'help':
            await Help.ignore(self, ctx)
        elif roleVar in ctx.author.roles:
            desc = ('You already have the Ignored role!')
            await error_embed(ctx, desc)
        else:
            await ctx.author.add_roles(roleVar)
            title = (f'Gave Ignored role to {ctx.message.author}.')
            desc = ('Your messages will not trigger most of the response regexes now.')
            await channel_embed(ctx, title, desc)
            logging.info(f'{ctx.author.id} gave themselfs ignore role')

    @commands.command()
    async def unignore(self, ctx, elp=None):
        roleVar = discord.utils.get(ctx.guild.roles, id=ignoreRole)
        if elp == 'help':
            await Help.ignore(self, ctx)
        elif roleVar not in ctx.author.roles:
            desc = ("You don't have the Ignored role!")
            await error_embed(ctx, desc)
        else:
            await ctx.author.remove_roles(roleVar)
            title = (f'Removed Ignored role from {ctx.message.author}.')
            desc = ('Your messages will now trigger most of the response regexes.')
            await channel_embed(ctx, title, desc)
            logging.info(f'{ctx.author.id} removed ignore role')

    @commands.command()
    async def releases(self, ctx, elp=None):
        roleVar = discord.utils.get(ctx.guild.roles, id=releasesRole)
        if elp == 'help':
            await Help.releases(self, ctx)
        elif roleVar in ctx.author.roles:
            desc = ('You already have the Releases role!')
            await error_embed(ctx, desc)
        else:
            await ctx.author.add_roles(roleVar)
            title = (f'Gave Releases role to {ctx.message.author}.')
            desc = ('You will now be pinged when a new release is made!')
            await channel_embed(ctx, title, desc)
            logging.info(f'{ctx.author.id} gave themselfs releases role')

    @commands.command()
    async def unreleases(self, ctx, elp=None):
        roleVar = discord.utils.get(ctx.guild.roles, id=releasesRole)
        if elp == 'help':
            await Help.releases(self, ctx)
        elif roleVar not in ctx.author.roles:
            desc = ("You don't have the Releases role!")
            await error_embed(ctx, desc)
        else:
            await ctx.author.remove_roles(roleVar)
            title = (f'Removed Releases role from {ctx.message.author}.')
            desc = ('You now will not be pinged when a new release is made .')
            await channel_embed(ctx, title, desc)
            logging.info(f'{ctx.author.id} removed releases role')
    
    @ignore.error
    @unignore.error
    @releases.error
    @unreleases.error
    async def role_error(self, ctx, error):
        desc = None
        await error_embed(ctx, desc, error)
        logging.info(f'{ctx.author.id} tried to add/remove releases/ignore but it gave the error: {error}')

def setup(bot):
    bot.add_cog(Roles(bot))