import discord
from discord.ext import commands
from main import mod_group, channel_embed, error_embed
from cogs.help import Help


class Embed(commands.Cog):
    def __init__(self, bot):
        """Returns embeds for the embed command."""
        self.bot = bot

    @commands.group(invoke_without_command=True, case_insensitive=True, aliases=['eb'])
    @commands.check(mod_group)
    async def embed(self, ctx, channel: discord.TextChannel = None, etitle=None, *, edesc=None):
        if channel is None:
            return await Help.embed(self, ctx)
        if etitle is None:
            await error_embed(ctx, 'You need to give a title')
        elif edesc is None:
            await error_embed(ctx, 'You need to give a description')
        else:
            await channel_embed(channel, etitle, edesc)
            print(f'{ctx.author.id} sent a custom embed to a channel')

    @embed.command(aliases=['h'])
    @commands.check(mod_group)
    async def here(self, ctx, etitle=None, *, edesc=None):
        if etitle is None:
            await error_embed(ctx, 'You need to give a title')
        elif edesc is None:
            await error_embed(ctx, 'You need to give a description')
        else:
            await channel_embed(ctx.channel, etitle, edesc)
            print(f'{ctx.author.id} sent a custom embed to a channel')


def setup(bot):
    bot.add_cog(Embed(bot))
