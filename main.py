import glob
import logging

import discord
from discord.ext import commands

from database import DB
from utils import GITHUB_TOKEN, GUILD_ID, PRESENCE_ACTION_KEY, DISCORD_TOKEN


class Bot(commands.Bot):
    def __init__(self):

        # I don't want there to be a prefix so the bell ascii character is put here as you can't send that in discord
        super().__init__(intents=discord.Intents.all(), command_prefix='\a')
        self.db: DB = DB()

    async def setup_hook(self):
        # start up the database
        await bot.db.connect_to_db()
        log.info('connected to the database')

        # load extensions
        for folder_name in glob.glob('*/'):
            for file_name in glob.glob(folder_name + '/*'):
                if file_name.endswith('.py') and file_name[:5] != 'utils' and file_name[:8] != 'database':
                    if not GITHUB_TOKEN and 'github' in file_name:
                        # We don't want to load GitHub commands without a GitHub token
                        log.info('GitHub token is not present, skipped loading GitHub extension')
                        continue
                    await bot.load_extension(file_name[:-3].replace('\\', '.').replace('/', '.'))
                    log.info(f'loaded extension {file_name}')

        # make commands only available in a specific server
        self.tree.copy_global_to(guild=discord.Object(id=GUILD_ID))
        await self.tree.sync(guild=discord.Object(id=GUILD_ID))
        log.info(f'synced commands to guild: {GUILD_ID}')


discord.utils.setup_logging(level=logging.INFO)
log = logging.getLogger('main')
bot = Bot()


@bot.event
async def on_ready():
    bot.db.set_bot_id(bot.user.id)

    # change presence to what's in the db
    await bot.change_presence(
        activity=discord.Activity(type=PRESENCE_ACTION_KEY[bot.db.presence_action], name=bot.db.presence_value)
    )
    log.info('bot is now ready, set the db bot_id and changed the presence')

bot.run(DISCORD_TOKEN, log_handler=None)
