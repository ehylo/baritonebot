import os
from dotenv import load_dotenv

import discord

load_dotenv()

# environment variables
GUILD_ID = int(os.getenv('GUILD_ID'))
DATABASE_URL = os.getenv('DATABASE_URL')
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
PASTE_TOKEN = os.getenv('PASTE_TOKEN')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

# other stuff
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
VERSION_183_URL = 'https://raw.githubusercontent.com/cabaletta/baritone/v1.8.3/src/api/java/baritone/api/Settings.java'
VERSION_1215_URL = 'https://raw.githubusercontent.com/cabaletta/baritone/v1.2.15/src/api/java/baritone/api/Settings.java'
VERSION_19_URL = 'https://raw.githubusercontent.com/wagyourtail/baritone/1.19/1.19.2/src/api/java/baritone/api/Settings.java'

# defaults
DEFAULT_EMBED_COLOR = '81C3FF'
DEFAULT_PRESENCE_ACTION = 'Watching'
DEFAULT_PRESENCE_VALUE = 'humans interact'
