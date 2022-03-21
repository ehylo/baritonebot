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
    1: discord.ActivityType.watching,
    2: discord.ActivityType.playing,
    3: discord.ActivityType.listening,
    4: discord.ActivityType.competing
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
VERSION_182_URL = ''
VERSION_1215_URL = ''
VERSION_172_URL = ''
VERSION_163_URL = ''

# defaults
DEFAULT_EMBED_COLOR = '81C3FF'
DEFAULT_PREFIX = 'b?'
DEFAULT_PRESENCE_ACTION = 1
DEFAULT_PRESENCE_VALUE = 'humans interact'
