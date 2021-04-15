from discord.ext import commands
from cogs.help import Help
from cogs.const import channel_embed


class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def ping(self, ctx):
        await channel_embed(ctx, f'Pong! 🏓 ({round(self.bot.latency * 1000)}ms)', None)

    @ping.command()
    async def help(self, ctx):
        await Help.ping(self, ctx)


def setup(bot):
    bot.add_cog(Ping(bot))
