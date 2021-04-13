import discord
import os
import logging
import shutil
import json
from discord.ext import commands

''' create these files if they do not exist '''

if os.path.exists('./data/values.json') == False:
    shutil.copyfile(r'./data/default-values.json', r'./data/values.json')
    print("data/values.json was created, please fill out the token, paste token, prefix, and color embed")
    quit()
if os.path.exists('./data/rules.json') == False:
    shutil.copyfile(r'./data/default-rules.json', r'./data/rules.json')
if os.path.exists('./data/responses.json') == False:
    shutil.copyfile(r'./data/default-responses.json', r'./data/responses.json')
open('./data/cringe.txt', 'a').close()
open('./data/exemptchannels.txt', 'a').close()
open('./data/blacklist.txt', 'a').close()


with open('./data/values.json') as jsonValues:
    valuesStr = json.load(jsonValues)
    token = str((valuesStr)[0]['token'])
    setPresence = str((valuesStr)[0]['presence'])
    preCmd = str((valuesStr)[0]['prefix'])

bot = commands.Bot(command_prefix=preCmd, intents=discord.Intents.all())
bot.remove_command('help')

for filename in os.listdir('./cogs'):
    if filename.endswith('__init__.py'):
        logging.info('[STARTUP] skipped loading __init__.py file because it is not an extension')
    elif filename.endswith('const.py'):
        logging.info('[STARTUP] skipped loading const.py file because it is not an extension')
    elif filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')
logging.info('[STARTUP] loaded all extensions')

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=setPresence))
    logging.info('[STARTUP] Successfully started baritoe bot and set the presence according to the values.json')

bot.run(token)