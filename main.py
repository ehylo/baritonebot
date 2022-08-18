import glob

import discord
from discord.ext import commands

from utils.db import DB
from utils import const
from utils.baritone_settings import VersionSettings

bot_db = DB()
baritone_settings_v2 = VersionSettings(const.VERSION_1215_URL)
baritone_settings_v8 = VersionSettings(const.VERSION_183_URL)
baritone_settings_v9 = VersionSettings(const.VERSION_19_URL)

version_matcher = {
    '1.2.15': baritone_settings_v2,
    '1.9': baritone_settings_v9,
    '1.8.3': baritone_settings_v8
}

bot = commands.Bot(
    case_insensitive=True,
    intents=discord.Intents.all()
)

# load the cogs
for folder_name in glob.glob('*/'):
    for file_name in glob.glob(folder_name + '/*'):
        if file_name.endswith('.py') and not file_name.startswith('utils'):
            bot.load_extension(file_name[:-3].replace('\\', '.').replace('/', '.'), store=False)


@bot.event
async def on_ready():
    bot_db.update_bot_id(bot.user.id)
    await bot.change_presence(
        activity=discord.Activity(type=const.PRESENCE_ACTION_KEY[bot_db.presence_action], name=bot_db.presence_value)
    )
    print('started')

bot.run(const.DISCORD_TOKEN)
