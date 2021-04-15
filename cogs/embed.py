import logging

import discord
from discord.ext import commands
from cogs.const import mod_group, channel_embed, error_embed
from cogs.help import Help


class Embed(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    @commands.check(mod_group)
    async def embed(self, ctx, send_channel=None, etitle=None, *, edesc=None):
        channel_str = str(ctx.message.raw_channel_mentions)[1:-1]
        if send_channel is None:
            await Help.embed(self, ctx)
        elif etitle is None:
            await error_embed(ctx, 'You need to give a title')
        elif edesc is None:
            await error_embed(ctx, 'You need to give a description')
        else:
            if channel_str == '':
                try:
                    int(send_channel)
                    channel = await self.bot.fetch_channel(send_channel)
                    await channel_embed(ctx, etitle, edesc, channel)
                    logging.info(f'{ctx.author.id} sent a custom embed to a channel')
                except ValueError:
                    await error_embed(ctx, 'That is not a valid ID (use **numbers**)')
                except discord.NotFound:
                    await error_embed(ctx, 'Invalid channel ID')
                except discord.Forbidden:
                    await error_embed(ctx, 'I do not have access to that channel')
            else:
                try:
                    channel_id = int(channel_str)
                    channel = await self.bot.fetch_channel(channel_id)
                    await channel_embed(ctx, etitle, edesc, channel)
                    logging.info(f'{ctx.author.id} sent a custom embed to a channel')
                except discord.Forbidden:
                    await error_embed(ctx, 'I do not have access to that channel')

    @embed.command()
    @commands.check(mod_group)
    async def here(self, ctx, etitle=None, *, edesc=None):
        if etitle is None:
            await error_embed(ctx, 'You need to give a title')
        elif edesc is None:
            await error_embed(ctx, 'You need to give a description')
        else:
            await channel_embed(ctx, etitle, edesc)
            logging.info(f'{ctx.author.id} sent a custom embed to a channel')


def setup(bot):
    bot.add_cog(Embed(bot))
