import discord
import os
import logging
from dotenv import load_dotenv
from discord.ext import commands
from cogs.const import setPresence, preCmd

load_dotenv()
token = os.getenv('token')

bot = commands.Bot(command_prefix=preCmd, intents=discord.Intents.all())
bot.remove_command('help')

'''Load cogs'''

for filename in os.listdir('./cogs'):
    if filename.endswith('__init__.py'):
        logging.info('[STARTUP] skipped loading __init__.py file because it is not an extension') #not a cog
    elif filename.endswith('const.py'):
        logging.info('[STARTUP] skipped loading const.py file because it is not an extension') #not a cog
    elif filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')
logging.info('[STARTUP] loaded all extensions')

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=setPresence))
    logging.info('[STARTUP] Successfully started baritoe bot and set the presence according to the values.json')

bot.run(token)