import discord
import main
from discord.ext import commands
from cogs.help import Help


async def role_add(self, ctx, arg, role, role_words, action):
    if (arg is not None) and (arg.lower() == 'help'):
        await Help.ignore(self, ctx)
    else:
        b_guild = self.bot.get_guild(main.ids[1])
        member_check = b_guild.get_member(ctx.author.id)
        b_role = discord.utils.get(b_guild.roles, id=role)
        if action == 'remove':
            if b_role not in member_check.roles:
                await main.error_embed(ctx, role_words)
            else:
                await member_check.remove_roles(b_role)
                return True
        elif action == 'add':
            if b_role in member_check.roles:
                await main.error_embed(ctx, role_words)
            else:
                await member_check.add_roles(b_role)
                return True


class Role(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ignore(self, ctx, arg=None):
        if await role_add(self, ctx, arg, main.ids[11], 'You already have the Ignore role', 'add') is True:
            await main.channel_embed(ctx, 'Ignored role obtained', 'Your messages will not trigger the response regexes unless you ping me')
            print(f'{ctx.author.id} gave themselfs ignore role')

    @commands.command()
    async def unignore(self, ctx, arg=None):
        if await role_add(self, ctx, arg, main.ids[11], 'You don\'t have the Ignore role', 'remove') is True:
            await main.channel_embed(ctx, 'Ignored role removed', 'Your messages will now trigger the response regexes.')
            print(f'{ctx.author.id} removed ignore role')

    @commands.command()
    async def releases(self, ctx, arg=None):
        if await role_add(self, ctx, arg, main.ids[13], 'You already have the Releases role', 'add') is True:
            await main.channel_embed(ctx, 'Releases role obtained', 'You will now be pinged when a new release is made!')
            print(f'{ctx.author.id} gave themselfs releases role')

    @commands.command()
    async def unreleases(self, ctx, arg=None):
        if await role_add(self, ctx, arg, main.ids[13], 'You don\'t have the Releases role', 'remove') is True:
            await main.channel_embed(ctx, 'Releases role removed', 'You now will not be pinged when a new release is made .')
            print(f'{ctx.author.id} removed releases role')


def setup(bot):
    bot.add_cog(Role(bot))
