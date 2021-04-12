import discord
import logging
from discord.ext import commands
from cogs.help import Help
from cogs.const import mod_group, channel_embed, error_embed, help_embed

class Embed(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    @commands.check(mod_group)
    async def embed(self, ctx, sendChannel=None, etitle=None, *, edesc=None):
        channelStr = str(ctx.message.raw_channel_mentions)[1:-1]
        channel = ctx.channel
        if sendChannel == None:
            await Help.embed(self, ctx)
        elif etitle == None:
            desc = ('You need to give a title')
            await error_embed(ctx, desc)
        elif edesc == None:
            desc = ('You need to give a description')
            await error_embed(ctx, desc,)
        else:
            if channelStr == '':
                try:
                    channelInt = int(sendChannel)
                    try:
                        channel = await self.bot.fetch_channel(channelInt)
                        desc = edesc
                        title = etitle
                        await channel_embed(ctx, title, desc, channel)
                        logging.info(f'{ctx.author.id} sent a custom embed to a channel')
                    except:
                        desc = ('That is not a valid channel ID')
                        await error_embed(ctx, desc)
                except:
                    desc = ('That is not a valid channel ID (use **numbers**)')
                    await error_embed(ctx, desc)
            else:
                channelId = int(channelStr)
                try:
                    channel = await self.bot.fetch_channel(channelId)
                    desc = edesc
                    title = etitle
                    await channel_embed(ctx, title, desc, channel)
                    logging.info(f'{ctx.author.id} sent a custom embed to a channel')
                except:
                    desc = ('Cannot send to that channel')
                    await error_embed(ctx, desc)
    
    @embed.command()
    @commands.check(mod_group)
    async def here(self, ctx, etitle=None, *, edesc=None):
        desc = edesc
        title = etitle
        await channel_embed(ctx, title, desc)
        logging.info(f'{ctx.author.id} sent a custom embed to a channel')

    @embed.error
    @here.error
    async def embed_error(self, ctx, error):
        if isinstance(error, commands.errors.CheckFailure):
            desc = (f'You need to be a Moderator to use the command `{ctx.command}`')
            await error_embed(ctx, desc)
        else:
            desc = None
            await error_embed(ctx, desc, error)
            logging.info(f'{ctx.author.id} tried to send an embed but it gave the error: {error}')

def setup(bot):
    bot.add_cog(Embed(bot))