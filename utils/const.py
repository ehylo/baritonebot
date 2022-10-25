import enum
import os
from dotenv import load_dotenv

import discord

from utils.baritone_settings import VersionSettings

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
VERSION_MASTER_URL = 'https://raw.githubusercontent.com/cabaletta/baritone/master/src/api/java/baritone/api/Settings.java'
VERSION_1215_URL = 'https://raw.githubusercontent.com/cabaletta/baritone/v1.2.15/src/api/java/baritone/api/Settings.java'
VERSION_183_URL = 'https://raw.githubusercontent.com/cabaletta/baritone/v1.8.3/src/api/java/baritone/api/Settings.java'
VERSION_19_URL = 'https://raw.githubusercontent.com/cabaletta/baritone/1.19.1/src/api/java/baritone/api/Settings.java'
VERSION_DOCS_URL = VERSION_1215_URL

# defaults
DEFAULT_EMBED_COLOR = '81C3FF'
DEFAULT_PRESENCE_ACTION = 'Watching'
DEFAULT_PRESENCE_VALUE = 'humans interact'

# baritone settings
baritone_settings_master = VersionSettings(VERSION_MASTER_URL)
baritone_settings_v2 = VersionSettings(VERSION_1215_URL)
baritone_settings_v8 = VersionSettings(VERSION_183_URL)
baritone_settings_v9 = VersionSettings(VERSION_19_URL)

baritone_settings_matcher = [
    ('master', baritone_settings_master),
    ('1.2.15', baritone_settings_v2),
    ('1.8.3', baritone_settings_v8),
    ('1.9', baritone_settings_v9),
]
baritone_settings_versions = enum.Enum(value='version', names=baritone_settings_matcher)
