import discord
import logging
from discord.ext import commands
from cogs.help import Help
from cogs.const import ignoreRole, releasesRole, channel_embed, error_embed, baritoneDiscord


class Ignore(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def ignore(self, ctx):
        b_guild = self.bot.get_guild(baritoneDiscord)
        member_check = b_guild.get_member(ctx.author.id)
        if member_check is None:
            await error_embed(ctx, 'You are not in the baritone discord which is required to recieve the Ignored role')
        else:
            b_role = discord.utils.get(b_guild.roles, id=ignoreRole)
            if b_role in member_check.roles:
                await error_embed(ctx, 'You already have the Ignored role!')
            else:
                await member_check.add_roles(b_role)
                await channel_embed(ctx, f'Ignored role obtained', 'Your messages will not trigger most of the response regexes now.')
                logging.info(f'{ctx.author.id} gave themselfs ignore role')

    @ignore.command()
    async def help(self, ctx):
        await Help.ignore(self, ctx)


class Unignore(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def unignore(self, ctx):
        b_guild = self.bot.get_guild(baritoneDiscord)
        member_check = b_guild.get_member(ctx.author.id)
        if member_check is None:
            await error_embed(ctx, 'You are not in the baritone discord which is required to remove the Ignored role')
        else:
            b_role = discord.utils.get(b_guild.roles, id=ignoreRole)
            if b_role not in member_check.roles:
                await error_embed(ctx, 'You don\'t have the Ignored role!')
            else:
                await member_check.remove_roles(b_role)
                await channel_embed(ctx, f'Ignored role lost', 'Your messages will now trigger most of the response regexes.')
                logging.info(f'{ctx.author.id} removed ignore role')
        
    @unignore.command()
    async def help(self, ctx):
        await Help.ignore(self, ctx)


class Releases(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def releases(self, ctx):
        b_guild = self.bot.get_guild(baritoneDiscord)
        member_check = b_guild.get_member(ctx.author.id)
        if member_check is None:
            await error_embed(ctx, 'You are not in the baritone discord which is required to recieve the Releases role')
        else:
            b_role = discord.utils.get(b_guild.roles, id=releasesRole)
            if b_role in member_check.roles:
                await error_embed(ctx, 'You already have the Releases role!')
            else:
                await member_check.add_roles(b_role)
                await channel_embed(ctx, 'Releases role obtained', 'You will now be pinged when a new release is made!')
                logging.info(f'{ctx.author.id} gave themselfs releases role')

    @releases.command()
    async def help(self, ctx):
        await Help.releases(self, ctx)


class Unreleases(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def unreleases(self, ctx):
        b_guild = self.bot.get_guild(baritoneDiscord)
        member_check = b_guild.get_member(ctx.author.id)
        if member_check is None:
            await error_embed(ctx, 'You are not in the baritone discord which is required to remove the Releases role')
        else:
            ignore = discord.utils.get(b_guild.roles, id=releasesRole)
            if ignore not in member_check.roles:
                await error_embed(ctx, 'You don\'t have the Releases role!')
            else:
                await member_check.remove_roles(ignore)
                await channel_embed(ctx, 'Releases role lost', 'You now will not be pinged when a new release is made .')
                logging.info(f'{ctx.author.id} removed releases role')

    @unreleases.command()
    async def help(self, ctx):
        await Help.releases(self, ctx)


def setup(bot):
    bot.add_cog(Ignore(bot))
    bot.add_cog(Unignore(bot))
    bot.add_cog(Releases(bot))
    bot.add_cog(Unreleases(bot))
