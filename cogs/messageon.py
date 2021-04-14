import discord
import logging
import requests
import js_regex
import re
import json
from cogs.const import preCmd, logChannel, log_embed, channel_embed, pasteToken, bbi, ignoreRole, baritoneDiscord
from datetime import datetime, timedelta
from discord.ext import commands


async def del_blacklist(message, b_discord):
    if not message.content.startswith(preCmd):  # don't trigger when commands are used
        isdeleted = 0
        if isdeleted == 0:
            with open("./data/blacklist.txt", "r") as f:
                for line in [sub.replace('\n', '') for sub in (f.readlines())]:
                    if line in (re.sub(r"[\n]", "", message.content)):
                        await message.delete()
                        isdeleted += 1
        if (isdeleted == 0) and (len(message.attachments) > 0):  # don't make it a paste if it's deleted
            await att_paste(message)
        if isdeleted == 0:
            if b_discord.get_role(ignoreRole) not in message.author.roles:
                await gexre(message)
            elif b_discord.get_member(bbi) in message.mentions:
                await gexre(message)


async def dm_log(self, message):
    channel = await self.bot.fetch_channel(logChannel)
    await log_embed(message, f'I have recieved a DM', message.content, channel)
    logging.info(f'{message.author.id} dmed me \"{message.content}\"')


async def att_paste(message):
    if message.attachments[0].url.lower().endswith(('.log', '.txt', '.json')):
        text = await discord.Attachment.read(message.attachments[0], use_cached=False)
        paste_response = requests.post(url='https://api.paste.ee/v1/pastes', json={'sections': [{'name': "Paste from " + str(message.author), 'contents': ("\n".join((text.decode('UTF-8')).splitlines()))}]}, headers={'X-Auth-Token': pasteToken})
        actual_link = paste_response.json()
        await channel_embed(message.channel, 'Contents uploaded to paste.ee', (actual_link["link"]))
        logging.info(f'{message.author.id} uploaded a paste to {(actual_link["link"])}')


async def gexre(message):
    with open('./data/responses.json') as jsonResp:
        response_list = json.load(jsonResp)
    for x in range(1, (len(response_list)+1)):
        if js_regex.compile(response_list[x - 1]['regex']).search(message.content):
            await channel_embed(message.channel, (response_list[x - 1]['title']), (response_list[x - 1]['description']))


class Messageon(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        e_c = open("./data/exemptchannels.txt", "r")
        exempt_channels = e_c.read()
        e_c.close()
        b_discord = self.bot.get_guild(baritoneDiscord)
        if (message.author.id is not bbi) and (str(message.channel.id) not in exempt_channels) and (message.guild is not None):  # this avoids dms, exempted channels, and messages by itself
            await del_blacklist(message, b_discord)
        else:
            if len(message.attachments) > 0:
                await att_paste(message)
            if (message.guild is None) and (message.author.id != bbi):
                await dm_log(self, message)
                await gexre(message)
            elif b_discord.get_member(bbi) in message.mentions:
                await gexre(message)

        channel = await self.bot.fetch_channel(logChannel)
        async for message in channel.history():
            if (message.created_at + timedelta(hours=24)) < datetime.utcnow():
                await message.delete()
                logging.info('cleared logs older then 24 hours in the logs channel')
        await self.bot.process_commands(message)


def setup(bot):
    bot.add_cog(Messageon(bot))
