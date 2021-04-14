import discord
import json
import logging
import sys
import datetime

fault_footer = u'\U0001f916' 'Baritoe Bot' u'\U0001f916'
timeDate = datetime.datetime.utcnow()

with open('./data/values.json') as jsonValues:
    valuesStr = json.load(jsonValues)
    coolEmbedColor = int((valuesStr[0]['color']), 16)
    setPresence = str(valuesStr[0]['presence'])
    preCmd = str(valuesStr[0]['prefix'])
    pasteToken = str(valuesStr[0]['pasteToken'])

bbi = 823620099054239744
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


async def admin_group(ctx):
    try:
        adminrlist = [int(r.id) for r in ctx.author.roles]
        if adminrlist.count(adminRole) == 1 or adminrlist.count(devRole) == 1 or adminrlist.count(bypsRole) == 1:
            return True
        else:
            await error_embed(ctx, f'You need to be an Admin to use the command `{ctx.command}`')
    except AttributeError:
        await error_embed(ctx, f'You cannot use the command `{ctx.command}` in dms!')


async def mod_group(ctx):
    try:
        modRoleList = [int(r.id) for r in ctx.author.roles]
        if modRoleList.count(moderatorRole) == 1 or modRoleList.count(bypsRole) == 1:
            return True
        else:
            await error_embed(ctx, f'You need to be an Moderator to use the command `{ctx.command}`')
    except AttributeError:
        await error_embed(ctx, f'You cannot use the command `{ctx.command}` in dms!')


async def helper_group(ctx):
    try:
        helperRoleList = [int(r.id) for r in ctx.author.roles]
        if helperRoleList.count(helperRole) == 1 or helperRoleList.count(bypsRole) == 1:
            return True
        else:
            await error_embed(ctx, f'You need to be an Helper to use the command `{ctx.command}`')
    except AttributeError:
        await error_embed(ctx, f'You cannot use the command `{ctx.command}` in dms!')


async def error_embed(ctx, desc=None, error=None):
    embedVar = discord.Embed(color=coolEmbedColor, timestamp=timeDate, title='Error')
    if desc is None:
        desc = f'An unhandled error occured (probably bad): \n```{error}```'
    embedVar.description = desc
    embedVar.set_footer(text=fault_footer)
    await ctx.send(embed=embedVar)


async def log_embed(ctx=None, title=None, desc=None, channel=None, member=None):
    embedVar = discord.Embed(color=coolEmbedColor, timestamp=timeDate, desc=desc, title=title)
    if member is None:
        embedVar.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        embedVar.set_footer(text=f'{fault_footer} ID: {ctx.author.id}')
    else:
        embedVar.set_author(name=member, icon_url=member.avatar_url)
        embedVar.set_footer(text=f'{fault_footer} ID: {member.id}')
    await channel.send(embed=embedVar)


async def channel_embed(ctx, title=None, desc=None, channel=None):
    if title is None:
        title = 'PING FLURR TO FIX'
    embedVar = discord.Embed(color=coolEmbedColor, timestamp=timeDate, title=title)
    if desc is not None:
        embedVar.description = desc
    embedVar.set_footer(text=fault_footer)
    if channel is not None:
        await channel.send(embed=embedVar)
    else:
        await ctx.send(embed=embedVar)


async def help_embed(ctx, title, desc=None, fieldValue=None, fieldName=None):
    embedVar = discord.Embed(color=coolEmbedColor, timestamp=timeDate, title=title, description=desc)
    if fieldName is None:
        fieldName = 'Usage:'
    embedVar.add_field(name=fieldName, value=fieldValue, inline=False)
    embedVar.set_footer(text=fault_footer)
    await ctx.send(embed=embedVar)


async def dm_embed(ctx, dtitle, ddesc, dchannel):
    embedVar = discord.Embed(color=coolEmbedColor, timestamp=timeDate, title=dtitle, description=ddesc)
    embedVar.set_footer(text=fault_footer)
    await dchannel.send(embed=embedVar)


async def console(ctx, error):
    logging.error(f'{ctx.author.id} tried to use the command {ctx.command} but it gave the error: {error}')
