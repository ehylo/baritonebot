import glob

import discord
from discord.ext import commands

from utils.db import DB
from utils import const
from utils.baritone_settings import VersionSettings


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(intents=discord.Intents.all(), command_prefix=None)
        self.db = DB()
        self.baritone_settings_master = VersionSettings(const.VERSION_MASTER_URL)
        self.baritone_settings_v2 = VersionSettings(const.VERSION_1215_URL)
        self.baritone_settings_v8 = VersionSettings(const.VERSION_183_URL)
        self.baritone_settings_v9 = VersionSettings(const.VERSION_19_URL)

        self.version_matcher = {
            'master': self.baritone_settings_master,
            '1.2.15': self.baritone_settings_v2,
            '1.8.3': self.baritone_settings_v8,
            '1.9': self.baritone_settings_v9,
        }

    async def setup_hook(self):
        for folder_name in glob.glob('*/'):
            for file_name in glob.glob(folder_name + '/*'):
                if file_name.endswith('.py') and not file_name.startswith('utils'):
                    await bot.load_extension(file_name[:-3].replace('\\', '.').replace('/', '.'))
        self.tree.copy_global_to(guild=discord.Object(id=const.GUILD_ID))
        await self.tree.sync(guild=discord.Object(id=const.GUILD_ID))


bot = Bot()


@bot.event
async def on_ready():
    bot.db.update_bot_id(bot.user.id)
    await bot.change_presence(
        activity=discord.Activity(type=const.PRESENCE_ACTION_KEY[bot.db.presence_action], name=bot.db.presence_value)
    )
    print('started')

bot.run(const.DISCORD_TOKEN)
