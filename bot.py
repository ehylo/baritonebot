import discord
import os
import logging
import psycopg2
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
token = os.getenv('token')
pasteToken = os.getenv('paste_token')
DATABASE_URL = os.getenv('DATABASE_URL')

db = psycopg2.connect(DATABASE_URL, sslmode='require')
cur = db.cursor()
cur.execute('SELECT * FROM settings')
values = cur.fetchone()
db.close()

bot = commands.Bot(command_prefix=values[0], intents=discord.Intents.all())
bot.remove_command('help')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')
logging.info('[STARTUP] loaded all extensions')


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=values[3]))
    logging.info('[STARTUP] Successfully started baritoe bot and set the presence and prefix to the default')

bot.run(token)
