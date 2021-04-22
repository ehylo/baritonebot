import discord
import logging
import sys
import os
import psycopg2
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
pasteToken = os.getenv('paste_token')

db = psycopg2.connect(DATABASE_URL, sslmode='require')
cur = db.cursor()
cur.execute(f'SELECT * FROM settings')
values = cur.fetchone()

fault_footer = u'\U0001f916' 'Baritone Bot' u'\U0001f916'
timeDate = datetime.utcnow()
coolEmbedColor = int(values[1], 16)

botID = 823620099054239744  # not adding these to values.json that way its easier to add more later on
helperRole = 826950651698610200  # currently set to my test server aswell, will need to change when bot gets added
devRole = 826950651711979530
bypassRole = 826950651711979531
moderatorRole = 826950651698610201
adminRole = 826950651698610204
ignoreRole = 826954212059381810
muteRole = 826950651690745885
releasesRole = 829556104274509875
voiceRole = 826954171961704458
leaveChannel = 826950652516106242
logChannel = 826950652516106245
baritoneDiscord = 826950651690745876

logging.basicConfig(filename='console.log', level=logging.INFO, format='[%(asctime)s %(levelname)s] %(message)s', datefmt='%m-%d-%Y %H:%M:%S')
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))


async def perms_check(ctx, required_role):
    if required_role == 'admin':
        for x in [adminRole, devRole, bypassRole]:
            if ctx.bot.get_guild(baritoneDiscord).get_role(x) in ctx.bot.get_guild(baritoneDiscord).get_member(ctx.author.id).roles:
                return True
        else:
            await error_embed(ctx, f'You need to be an Admin to use the command `{ctx.command}`')
    if required_role == 'mod':
        for x in [moderatorRole, adminRole, devRole, bypassRole]:
            if ctx.bot.get_guild(baritoneDiscord).get_role(x) in ctx.bot.get_guild(baritoneDiscord).get_member(ctx.author.id).roles:
                return True
        else:
            await error_embed(ctx, f'You need to be an Moderator to use the command `{ctx.command}`')
    if required_role == 'helper':
        for x in [helperRole, moderatorRole, adminRole, devRole, bypassRole]:
            if ctx.bot.get_guild(baritoneDiscord).get_role(x) in ctx.bot.get_guild(baritoneDiscord).get_member(ctx.author.id).roles:
                return True
        else:
            await error_embed(ctx, f'You need to be an Helper to use the command `{ctx.command}`')


async def admin_group(ctx):
    if await perms_check(ctx, 'admin'):
        return True


async def mod_group(ctx):
    if await perms_check(ctx, 'mod'):
        return True


async def helper_group(ctx):
    if await perms_check(ctx, 'helper'):
        return True


async def error_embed(ctx, desc=None, error=None):
    em_v = discord.Embed(color=16711680, timestamp=timeDate, title='Error')
    if desc is None:
        desc = f'An unhandled error occured (probably bad): \n```{error}```'
    em_v.description = desc
    em_v.set_footer(text=fault_footer)
    await ctx.send(embed=em_v)


async def log_embed(ctx=None, title=None, desc=None, channel=None, member=None):
    if title is None:
        title = ''
    em_v = discord.Embed(color=coolEmbedColor, timestamp=timeDate, title=title)
    em_v.description = desc
    if member is None:
        em_v.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        em_v.set_footer(text=f'{fault_footer} ID: {ctx.author.id}')
    else:
        em_v.set_author(name=member, icon_url=member.avatar_url)
        em_v.set_footer(text=f'{fault_footer} ID: {member.id}')
    await channel.send(embed=em_v)


async def channel_embed(ctx, title=None, desc=None, thumbnail=None, replyorsend=None):
    em_v = discord.Embed(color=coolEmbedColor, timestamp=timeDate, title=title)
    if desc is not None:
        em_v.description = desc
    em_v.set_footer(text=fault_footer)
    if thumbnail is not None:
        em_v.set_thumbnail(url=thumbnail)
    if replyorsend is not None:
        bot_reply = await ctx.reply(embed=em_v)
        await bot_reply.add_reaction('🗑️')
    else:
        await ctx.send(embed=em_v)


async def help_embed(ctx, title, desc=None, field_value=None, field_name=None, image=None):
    em_v = discord.Embed(color=coolEmbedColor, timestamp=timeDate, title=title, description=desc)
    if image is not None:
        em_v.set_image(url=image)
    if field_name is None:
        field_name = 'Usage:'
    em_v.add_field(name=field_name, value=field_value, inline=False)
    em_v.set_footer(text=fault_footer)
    await ctx.send(embed=em_v)


async def dm_embed(dtitle, ddesc, dchannel):
    em_v = discord.Embed(color=coolEmbedColor, timestamp=timeDate, title=dtitle, description=ddesc)
    em_v.set_footer(text=fault_footer)
    await dchannel.send(embed=em_v)
