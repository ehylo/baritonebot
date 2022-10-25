import glob

import discord
from discord.ext import commands

from utils.db import DB
from utils import const


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(intents=discord.Intents.all(), command_prefix=None)
        self.db = DB()

    async def setup_hook(self):
        # load extensions
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
