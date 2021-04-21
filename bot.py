import discord
import os
import logging
import sqlite3
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
token = os.getenv('token')
pasteToken = os.getenv('paste_token')

open('main.sqlite', 'a').close()  # create db file if it does not exist
db = sqlite3.connect('main.sqlite')
cur = db.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS blacklist(blacklist_word text)')  # create all of the tables if they do not exist
cur.execute('CREATE TABLE IF NOT EXISTS cringe(cringe_link text)')
cur.execute('CREATE TABLE IF NOT EXISTS settings(prefix text, embedcolor text, presencetype text, presence text, yes text)')
cur.execute('CREATE TABLE IF NOT EXISTS ex_channels(channel_id integer)')
cur.execute('CREATE TABLE IF NOT EXISTS responses(response_regex text, response_title text, response_description text)')
cur.execute('CREATE TABLE IF NOT EXISTS rules(rules_number integer, rules_title text, rules_description text)')
cur.execute('SELECT prefix FROM settings WHERE yes="yes"')  # check if a row already exists for settings, there probably is a better way to do this but idc
if cur.fetchone() is None:
    cur.execute(f'INSERT INTO settings(prefix, embedcolor, presence, yes) VALUES(?,?,?,?)', ('b?', '81C3FF', 'humans interact', 'yes'))  # set some defaults
db.commit()
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
