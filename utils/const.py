import os
from dotenv import load_dotenv

import discord

load_dotenv()

GUILD_ID = int(os.getenv('GUILD_ID'))
DATABASE_URL = os.getenv('DATABASE_URL')
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
PASTE_TOKEN = os.getenv('PASTE_TOKEN')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
SCHEMA = os.getenv('DB_SCHEMA')

PRESENCE_ACTION_KEY = {
    'Watching': discord.ActivityType.watching,
    'Playing': discord.ActivityType.playing,
    'Listening to': discord.ActivityType.listening,
    'Competing in': discord.ActivityType.competing
}
TIME_KEYS = {
    'Seconds': 1,
    'Minutes': 60,
    'Hours': 3600,
    'Days': 86400,
    'Weeks': 604800,
}
FOUR_WEEKS = 2419200
RED_EMBED_COLOR = 16711680
HOISTED_CHARS = ('!', '"', '#', '$', '%', '&', '\'', '(', ')', '*', '+', ',', '-', '.', '/')

VERSION_MASTER_URL = 'https://raw.githubusercontent.com/cabaletta/baritone/master/src/api/java/baritone/api/Settings.java'
VERSION_12_URL = 'https://raw.githubusercontent.com/cabaletta/baritone/v1.2.17/src/api/java/baritone/api/Settings.java'
VERSION_LATEST_URL = 'https://raw.githubusercontent.com/cabaletta/baritone/1.20.1/src/api/java/baritone/api/Settings.java'
VERSION_DOCS_URL = VERSION_12_URL

DEFAULT_EMBED_COLOR = '81C3FF'
DEFAULT_PRESENCE_ACTION = 'Watching'
DEFAULT_PRESENCE_VALUE = 'humans interact'
