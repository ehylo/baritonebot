import asyncio
from datetime import datetime, timedelta

from discord.ext import commands, tasks

from utils import get_channel


class LogClear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.loops.start()

    def cog_unload(self):
        self.loops.cancel()

    @tasks.loop(seconds=60)
    async def loops(self):
        for guild in self.bot.guilds:

            # get the log channel for the specific guild
            log_channel = await get_channel(self.bot, self.bot.db.get_logs_channel_id(guild.id))

            # go through the messages in the log channel
            async for message in log_channel.history(limit=1000):

                # make sure the message is > 24 hours old
                if (message.created_at.replace(tzinfo=None) + timedelta(hours=24)) < datetime.utcnow():
                    await message.delete()

                    # sleep to avoid rate limits
                    await asyncio.sleep(1)

    @loops.before_loop
    async def before_loops(self):
        await self.bot.wait_until_ready()


async def setup(bot):
    await bot.add_cog(LogClear(bot))
