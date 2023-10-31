from datetime import datetime, timedelta
import asyncio

import discord.errors
from discord.ext import commands, tasks

from utils.misc import get_channel


class LogClear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.loops.start()

    def cog_unload(self):
        self.loops.cancel()

    @tasks.loop(seconds=5)
    async def loops(self):
        for guild_id in self.bot.db.logs_id:
            if self.bot.get_guild(guild_id) is not None:
                log_channel = await get_channel(self.bot, self.bot.db.logs_id[guild_id])
                try:
                    async for message in log_channel.history(limit=1000):
                        if (message.created_at.replace(tzinfo=None) + timedelta(hours=24)) < datetime.utcnow():
                            await message.delete()
                except discord.errors.DiscordServerError:
                    # These are normally rate limit problems so sleeping should someone limit this
                    await asyncio.sleep(2)

    @loops.before_loop
    async def before_loops(self):
        await self.bot.wait_until_ready()


async def setup(bot):
    await bot.add_cog(LogClear(bot))
