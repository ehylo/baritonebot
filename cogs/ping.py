import discord
import logging
from discord.ext import commands
from cogs.help import Help
from cogs.const import channel_embed, error_embed

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx, elp=None):
        if elp == 'help':
            await Help.ping(self, ctx)
        title = (f'Pong! 🏓 ({round(self.bot.latency * 1000)}ms)')
        desc = None
        await channel_embed(ctx, title, desc)
    
    @ping.error
    async def ping_error(self, ctx, error):
        desc = f'What the fuck how in the fuck did you get ping to cause an error? damn bro you get the broke ping role now *here is the error:* ```{error}```'
        await error_embed(ctx, desc, error)
        logging.info(f'{ctx.author.id} tried to ping but it gave the error: {error}')

def setup(bot):
    bot.add_cog(Ping(bot))