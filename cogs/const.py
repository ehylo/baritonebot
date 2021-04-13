import discord
import os
import json
import logging
import sys
import datetime
from discord.ext import commands

fault_footer = u'\U0001f916' 'Baritoe Bot' u'\U0001f916'
timeDate = datetime.datetime.utcnow()
bbi = (823620099054239744)

with open('./data/values.json') as jsonValues:
    valuesStr = json.load(jsonValues)
    coolEmbedColor = int(((valuesStr)[0]['color']), 16)
    setPresence = str((valuesStr)[0]['presence'])
    preCmd = str((valuesStr)[0]['prefix'])
    pasteToken = str((valuesStr)[0]['pasteToken'])

eC = open("./data/exemptchannels.txt", "r")
exmChl = eC.read()
eC.close()

logging.basicConfig(filename='console.log', level=logging.INFO, format='[%(asctime)s %(levelname)s] %(message)s', datefmt='%m-%d-%Y %H:%M:%S')
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

helperRole      =   (826950651698610200)
devRole         =   (826950651711979530)
bypsRole        =   (826950651711979531)
moderatorRole   =   (826950651698610201)
adminRole       =   (826950651698610204)
ignoreRole      =   (826954212059381810)
muteRole        =   (826950651690745885)
releasesRole    =   (829556104274509875)
voiceRole       =   (826954171961704458)
leaveChannel    =   (826950652516106242)
logChannel      =   (826950652516106245)
baritoneDiscord =   (826950651690745876)

async def admin_group(ctx):
    try:
        adminRoleList = [int(r.id) for r in ctx.author.roles]
        if adminRoleList.count(adminRole) == 1 or adminRoleList.count(devRole) == 1 or adminRoleList.count(bypsRole) == 1:
            return
        else:
            desc = (f'You need to be an Admin to use the command `{ctx.command}`')
            await error_embed(ctx, desc)
    except AttributeError:
        desc = (f'You cannot use the command `{ctx.command}` in dms!')
        await error_embed(ctx, desc)

async def mod_group(ctx):
    try:
        modRoleList = [int(r.id) for r in ctx.author.roles]
        if modRoleList.count(moderatorRole) == 1 or modRoleList.count(bypsRole) == 1:
            return
        else:
            desc = (f'You need to be an Moderator to use the command `{ctx.command}`')
            await error_embed(ctx, desc)
    except AttributeError:
        desc = (f'You cannot use the command `{ctx.command}` in dms!')
        await error_embed(ctx, desc)

async def helper_group(ctx):
    try:
        helperRoleList = [int(r.id) for r in ctx.author.roles]
        if helperRoleList.count(helperRole) == 1 or helperRoleList.count(bypsRole) == 1:
            return
        else:
            desc = (f'You need to be an Helper to use the command `{ctx.command}`')
            await error_embed(ctx, desc)
    except AttributeError:
        desc = (f'You cannot use the command `{ctx.command}` in dms!')
        await error_embed(ctx, desc)

async def error_embed(ctx, desc=None, error=None):
    dflt = (f'An unhandled error occured (probably bad): \n```{error}```')
    embedVar = discord.Embed(color = coolEmbedColor, timestamp=timeDate, title='Error')
    if desc == None:
        desc = dflt
    embedVar.description = (desc)
    embedVar.set_footer(text=(fault_footer))
    await ctx.send(embed=embedVar)

async def log_embed(ctx=None, title=None, desc=None, channel=None, member=None):
    embedVar = discord.Embed(color = coolEmbedColor, timestamp=timeDate)
    embedVar.description = (desc)
    embedVar.title = (title)
    if member == None:
        embedVar.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        embedVar.set_footer(text=(f'{fault_footer} ID: {ctx.author.id}'))
    else:
        embedVar.set_author(name=member, icon_url=member.avatar_url)
        embedVar.set_footer(text=(f'{fault_footer} ID: {member.id}'))
    await channel.send(embed=embedVar)

async def channel_embed(ctx, title=None, desc=None, channel=None):
    embedVar = discord.Embed(color = coolEmbedColor, timestamp=timeDate)
    if title == None:
        title = 'PING FLURR TO FIX'
    if desc != None:
        embedVar.description = (desc)
    embedVar.title = (title)
    embedVar.set_footer(text=(fault_footer))
    if channel is not None:
        await channel.send(embed=embedVar)
    else:
        await ctx.send(embed=embedVar)

async def help_embed(ctx, title, desc, fieldValue, fieldName=None):
    embedVar = discord.Embed(color = coolEmbedColor, timestamp=timeDate, title=title, description=desc)
    if fieldName == None:
        fieldName = 'Usage:'
    embedVar.add_field(name=fieldName, value=fieldValue, inline=False)
    embedVar.set_footer(text=(fault_footer))
    await ctx.send(embed=embedVar)

async def dm_embed(ctx, dtitle, ddesc, dchannel):
    embedVar = discord.Embed(color = coolEmbedColor, timestamp=timeDate, title=dtitle, description=ddesc)
    embedVar.set_footer(text=(fault_footer))
    await dchannel.send(embed=embedVar)