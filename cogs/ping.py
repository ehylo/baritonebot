from discord.ext import commands
from cogs.help import Help
from const import channel_embed


class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx, arg=None):
        if arg == 'help':
            await Help.ping(self, ctx)
        else:
            await channel_embed(ctx, f'Pong! 🏓 ({round(self.bot.latency * 1000)}ms)', None)


def setup(bot):
    bot.add_cog(Ping(bot))
