import discord
import json
import logging
import sys
import datetime

fault_footer = u'\U0001f916' 'Baritone Bot' u'\U0001f916'
timeDate = datetime.datetime.utcnow()

with open('./data/values.json') as jsonValues:
    valuesStr = json.load(jsonValues)
    coolEmbedColor = int((valuesStr[0]['color']), 16)
    setPresence = str(valuesStr[0]['presence'])
    preCmd = str(valuesStr[0]['prefix'])
    pasteToken = str(valuesStr[0]['pasteToken'])

bbi = 823620099054239744  # not adding these to values.json that way its easier to add more later on
helperRole = 826950651698610200
devRole = 826950651711979530
bypsRole = 826950651711979531
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


async def dm_check(ctx):
    try:
        [int(r.id) for r in ctx.author.roles]
        return True
    except AttributeError:
        await error_embed(ctx, f'You cannot use the command `{ctx.command}` in dms!')


async def perms_check(ctx, required_role):
    role_list = [int(r.id) for r in ctx.author.roles]
    if required_role == 'admin':
        if role_list.count(adminRole) == 1 or role_list.count(devRole) == 1 or role_list.count(bypsRole) == 1:
            return True
        else:
            await error_embed(ctx, f'You need to be an Admin to use the command `{ctx.command}`')
    if required_role == 'mod':
        if role_list.count(moderatorRole) == 1 or role_list.count(bypsRole) == 1:
            return True
        else:
            await error_embed(ctx, f'You need to be an Moderator to use the command `{ctx.command}`')
    if required_role == 'helper':
        if role_list.count(helperRole) == 1 or role_list.count(bypsRole) == 1:
            return True
        else:
            await error_embed(ctx, f'You need to be an Helper to use the command `{ctx.command}`')


async def admin_group(ctx):
    if await dm_check(ctx) is True:
        if await perms_check(ctx, 'admin'):
            return True


async def mod_group(ctx):
    if await dm_check(ctx) is True:
        if await perms_check(ctx, 'mod'):
            return True


async def helper_group(ctx):
    if await dm_check(ctx) is True:
        if await perms_check(ctx, 'helper'):
            return True


async def error_embed(ctx, desc=None, error=None):
    em_v = discord.Embed(color=coolEmbedColor, timestamp=timeDate, title='Error')
    if desc is None:
        desc = f'An unhandled error occured (probably bad): \n```{error}```'
    em_v.description = desc
    em_v.set_footer(text=fault_footer)
    await ctx.send(embed=em_v)


async def log_embed(ctx=None, title=None, desc=None, channel=None, member=None):
    em_v = discord.Embed(color=coolEmbedColor, timestamp=timeDate, title=title)
    em_v.description = desc
    if member is None:
        em_v.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        em_v.set_footer(text=f'{fault_footer} ID: {ctx.author.id}')
    else:
        em_v.set_author(name=member, icon_url=member.avatar_url)
        em_v.set_footer(text=f'{fault_footer} ID: {member.id}')
    await channel.send(embed=em_v)


async def channel_embed(ctx, title=None, desc=None, channel=None):
    if title is None:
        title = 'PING FLURR TO FIX'
    em_v = discord.Embed(color=coolEmbedColor, timestamp=timeDate, title=title)
    if desc is not None:
        em_v.description = desc
    em_v.set_footer(text=fault_footer)
    if channel is not None:
        await channel.send(embed=em_v)
    else:
        await ctx.send(embed=em_v)


async def help_embed(ctx, title, desc=None, field_value=None, field_name=None):
    em_v = discord.Embed(color=coolEmbedColor, timestamp=timeDate, title=title, description=desc)
    if field_name is None:
        field_name = 'Usage:'
    em_v.add_field(name=field_name, value=field_value, inline=False)
    em_v.set_footer(text=fault_footer)
    await ctx.send(embed=em_v)


async def dm_embed(dtitle, ddesc, dchannel):
    em_v = discord.Embed(color=coolEmbedColor, timestamp=timeDate, title=dtitle, description=ddesc)
    em_v.set_footer(text=fault_footer)
    await dchannel.send(embed=em_v)
