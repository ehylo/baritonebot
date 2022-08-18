from datetime import datetime, timedelta
from discord.ext import commands, tasks

from main import bot_db
from utils.misc import get_channel


class LogClear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.loops.start()

    def cog_unload(self):
        self.loops.cancel()

    @tasks.loop(seconds=5)
    async def loops(self):
        for guild_id in bot_db.logs_id:
            if self.bot.get_guild(guild_id) is not None:
                log_channel = await get_channel(self.bot, bot_db.logs_id[guild_id])
                async for message in log_channel.history(limit=1000):
                    if (message.created_at.replace(tzinfo=None) + timedelta(hours=24)) < datetime.utcnow():
                        await message.delete()

    @loops.before_loop
    async def before_loops(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(LogClear(bot))
