import discord
import os
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
cur.execute("SELECT id FROM ids WHERE guild='baritone' ORDER BY order_by")
ids = [int(item[0]) for item in cur.fetchall()]
print(ids[1])
coolEmbedColor = int(values[1], 16)

bot = commands.Bot(command_prefix=(values[0], values[0].upper()), case_insensitive=True, intents=discord.Intents.all())
bot.remove_command('help')


async def role_check(ctx, roles, name):
    for x in roles:
        if ctx.bot.get_guild(ids[1]).get_role(x) in ctx.bot.get_guild(ids[1]).get_member(ctx.author.id).roles:
            return True
    await error_embed(ctx, f'You need to be {name} to use the command `{ctx.command}`')


async def admin_group(ctx):
    if await role_check(ctx, [ids[8], ids[10], ids[7]], 'an Admin'):
        return True


async def mod_group(ctx):
    if await role_check(ctx, [ids[8], ids[10], ids[7], ids[9]], 'a Moderator'):
        return True


async def helper_group(ctx):
    if await role_check(ctx, [ids[8], ids[10], ids[7], ids[9], ids[6]], 'a Helper'):
        return True


async def error_embed(ctx, desc=None, error=None):
    em_v = discord.Embed(color=16711680, title='Error')
    if desc is None:
        desc = f'An unhandled error occured (probably bad): \n```{error}```'
    em_v.description = desc
    em_v.set_footer(text=f'{ctx.author.name} | ID: {ctx.author.id}', icon_url=ctx.author.avatar_url)
    await ctx.send(embed=em_v)


async def log_embed(ctx=None, title=None, desc=None, channel=None, member=None):
    if title is None:
        title = ''
    em_v = discord.Embed(color=coolEmbedColor, title=title)
    em_v.description = desc
    if ctx is None:
        ctx = member
    else:
        em_v.set_author(name=member, icon_url=member.avatar_url)
        ctx = ctx.author
    em_v.set_footer(text=f'{ctx.name} | ID: {ctx.id}', icon_url=ctx.avatar_url)
    await channel.send(embed=em_v)


async def channel_embed(ctx, title=None, desc=None, thumbnail=None, replyorsend=None):
    em_v = discord.Embed(color=coolEmbedColor, title=title)
    if desc is not None:
        em_v.description = desc
    if thumbnail is not None:
        em_v.set_thumbnail(url=thumbnail)
    if replyorsend is not None:
        em_v.set_footer(text=f'{ctx.author.name} | ID: {ctx.author.id}', icon_url=ctx.author.avatar_url)
        bot_reply = await ctx.reply(embed=em_v)
        await bot_reply.add_reaction('🗑️')
    else:
        if not hasattr(ctx, 'author'):
            pass
        else:
            em_v.set_footer(text=f'{ctx.author.name} | ID: {ctx.author.id}', icon_url=ctx.author.avatar_url)
            ctx = ctx.channel
        await ctx.send(embed=em_v)


async def help_embed(ctx, title, desc=None, field_value=None, field_name=None, image=None):
    em_v = discord.Embed(color=coolEmbedColor, title=title, description=desc)
    if image is not None:
        em_v.set_image(url=image)
    if field_name is None:
        field_name = 'Usage:'
    em_v.add_field(name=field_name, value=field_value, inline=False)
    em_v.set_footer(text=f'{ctx.author.name} | ID: {ctx.author.id}', icon_url=ctx.author.avatar_url)
    await ctx.send(embed=em_v)


async def dm_embed(dtitle, ddesc, dchannel):
    em_v = discord.Embed(color=coolEmbedColor, title=dtitle, description=ddesc)
    await dchannel.send(embed=em_v)

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')
print('[STARTUP] loaded all extensions')


@bot.event
async def on_ready():
    if values[2] == 'Watching':
        atype = discord.ActivityType.watching
    elif values[2] == 'Playing':
        atype = discord.ActivityType.playing
    elif values[2] == 'Listening to':
        atype = discord.ActivityType.listening
    else:
        atype = discord.ActivityType.competing
    await bot.change_presence(activity=discord.Activity(type=atype, name=values[3]))
    print('[STARTUP] Successfully started baritoe bot and set the presence and prefix to the default')

bot.run(token)