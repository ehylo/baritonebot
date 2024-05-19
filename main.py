import glob
import logging

import discord
from discord.ext import commands

from database import DB
from utils import GITHUB_TOKEN, GUILD_ID, PRESENCE_ACTION_KEY, DISCORD_TOKEN


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(intents=discord.Intents.all(), command_prefix='\a')
        self.db: DB = DB()

    async def setup_hook(self):
        # start up the database
        await bot.db.connect_to_db()

        # load extensions
        for folder_name in glob.glob('*/'):
            for file_name in glob.glob(folder_name + '/*'):
                if file_name.endswith('.py') and file_name[:5] != 'utils' and file_name[:8] != 'database':
                    if not GITHUB_TOKEN and 'github' in file_name:
                        # Don't want to load GitHub commands with no token
                        # TODO: Log that the github command wasn't loaded
                        continue
                    await bot.load_extension(file_name[:-3].replace('\\', '.').replace('/', '.'))

        # make commands only available in a specific server
        self.tree.copy_global_to(guild=discord.Object(id=GUILD_ID))
        await self.tree.sync(guild=discord.Object(id=GUILD_ID))


bot = Bot()


@bot.event
async def on_ready():
    bot.db.set_bot_id(bot.user.id)
    await bot.change_presence(
        activity=discord.Activity(type=PRESENCE_ACTION_KEY[bot.db.presence_action], name=bot.db.presence_value)
    )
    logging.warning('Bot has started.')

bot.run(DISCORD_TOKEN, log_level=logging.WARN)
