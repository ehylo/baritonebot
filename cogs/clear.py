import logging
from discord.ext import commands
from cogs.help import Help
from cogs.const import logChannel, log_embed, mod_group


class Clear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.check(mod_group)
    async def clear(self, ctx, limit: int = None):
        if limit is None:
            await Help.clear(self, ctx)
        else:
            await ctx.channel.purge(limit=limit)
            channel = await self.bot.fetch_channel(logChannel)
            await log_embed(ctx, 'Bulk messages deleted', f'Cleared {limit} messages in {ctx.channel.mention}', channel)
            logging.info(f'{ctx.author.id} cleared {limit} messages in {ctx.channel}')


def setup(bot):
    bot.add_cog(Clear(bot))
