from datetime import datetime, timedelta
from discord.ext import commands, tasks

from main import bot_db
from utils.misc import get_channel


class LogClear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @tasks.loop(seconds=5)
    async def loops(self):
        for guild_id in bot_db.logs_id:
            log_channel = await get_channel(self.bot, bot_db[guild_id])
            async for message in log_channel.history(after=datetime.utcnow() - timedelta(hours=24)):
                print(message.content)
                # await message.delete()  # lets not be annoying for right now


def setup(bot):
    bot.add_cog(LogClear(bot))
