import discord
import logging
from discord.ext import commands
from cogs.help import Help
from const import ignoreRole, releasesRole, channel_embed, error_embed, baritoneDiscord


async def role_add(self, ctx, arg, role, role_words, action):
    if (arg is not None) and (arg.lower() == 'help'):
        await Help.ignore(self, ctx)
    else:
        b_guild = self.bot.get_guild(baritoneDiscord)
        member_check = b_guild.get_member(ctx.author.id)
        b_role = discord.utils.get(b_guild.roles, id=role)
        if b_role in member_check.roles:
            await error_embed(ctx, role_words)
        else:
            if action == 'remove':
                await member_check.remove_roles(role)
            elif action == 'add':
                await member_check.add_roles(role)
            return True


class Role(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    """
    Commands for anyone to add/remove roles
    """

    @commands.command()
    async def ignore(self, ctx, arg=None):
        if await role_add(self, ctx, arg, ignoreRole, 'You already have the Ignore role', 'add') is True:
            await channel_embed(ctx, 'Ignored role obtained', 'Your messages will not trigger the response regexes unless you ping me')
            logging.info(f'{ctx.author.id} gave themselfs ignore role')

    @commands.command()
    async def unignore(self, ctx, arg=None):
        if await role_add(self, ctx, arg, ignoreRole, 'You don\'t have the Ignore role', 'remove') is True:
            await channel_embed(ctx, 'Ignored role removed', 'Your messages will now trigger the response regexes.')
            logging.info(f'{ctx.author.id} removed ignore role')

    @commands.command()
    async def releases(self, ctx, arg=None):
        if await role_add(self, ctx, arg, releasesRole, 'You already have the Releases role', 'add') is True:
            await channel_embed(ctx, 'Releases role obtained', 'You will now be pinged when a new release is made!')
            logging.info(f'{ctx.author.id} gave themselfs releases role')

    @commands.command()
    async def unreleases(self, ctx, arg=None):
        if await role_add(self, ctx, arg, releasesRole, 'You don\'t have the Releases role', 'remove') is True:
            await channel_embed(ctx, 'Releases role removed', 'You now will not be pinged when a new release is made .')
            logging.info(f'{ctx.author.id} removed releases role')


def setup(bot):
    bot.add_cog(Role(bot))
