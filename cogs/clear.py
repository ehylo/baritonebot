import discord
import logging
from discord.ext import commands
from cogs.help import Help
from cogs.const import logChannel, mod_group, help_embed, log_embed, error_embed

class Clear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.check(mod_group)
    async def clear(self, ctx, limit=None):
        if limit == None:
            await Help.clear(self, ctx)
        else:
            try:
                channel = await self.bot.fetch_channel(logChannel)
                clearNum = (int(limit))
                await ctx.channel.purge(limit=clearNum)
                title = 'Bulk messages deleted'
                desc = (f'Cleared {clearNum} messages in {ctx.channel.mention}')
                await log_embed(ctx, title, desc, channel)
                logging.info(f'{ctx.author.id} cleared {limit} messages in {ctx.channel}')
            except:
                desc = ('You need to give a **number** of messages to clear')
                await error_embed(ctx, desc)
        
    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.errors.CheckFailure):
            desc = (f'You need to be a Moderator to use the command `{ctx.command}`')
            await error_embed(ctx, desc)
        else:
            desc = None
            await error_embed(ctx, desc, error)
            logging.info(f'{ctx.author.id} tried to clear some messages in {ctx.channel} but it gave the error: {error}')

def setup(bot):
    bot.add_cog(Clear(bot))