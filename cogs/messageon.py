import discord
import logging
import requests
import js_regex
import re
import json
from bot import preCmd
from const import logChannel, log_embed, channel_embed, pasteToken, bbi, ignoreRole, baritoneDiscord, error_embed
from datetime import datetime, timedelta
from discord.ext import commands


async def del_blacklist(message, b_discord):
    e_c = open("./data/exemptchannels.txt", "r")
    exempt_channels = e_c.read()
    e_c.close()
    del_message = 0
    if del_message == 0:
        if (not message.content.startswith(preCmd) and              # don't delete commands
                message.author.id is not bbi and                    # don't delete messages from itself
                str(message.channel.id) not in exempt_channels and  # don't delete messages in exempted channels
                message.guild is not None):                         # don't try to delete dm messages
            with open("./data/blacklist.txt", "r") as f:
                for line in [sub.replace('\n', '') for sub in (f.readlines())]:
                    if line in (re.sub(r"[\n]", "", message.content)):
                        await message.delete()
                        del_message += 1
    if del_message == 0:
        await att_paste(message)
        await dm_log(message, b_discord)
        await gexre(message, b_discord, exempt_channels)


async def dm_log(message, b_discord):
    if (message.guild is None) and (message.author.id != bbi):
        channel = b_discord.get_channel(logChannel)
        await log_embed(message, f'I have recieved a DM', message.content, channel, None)
        logging.info(f'{message.author.id} dmed me \"{message.content}\"')


async def att_paste(message):
    if len(message.attachments) > 0:
        if message.attachments[0].url.lower().endswith(('.log', '.txt', '.json')):
            if pasteToken == "":
                await error_embed(message.channel,
                                  'There is no paste.ee API token in values.json so I am unable to upload that file for you')
            else:
                text = await discord.Attachment.read(message.attachments[0], use_cached=False)
                paste_response = requests.post(url='https://api.paste.ee/v1/pastes', json={'sections': [
                    {'name': "Paste from " + str(message.author),
                     'contents': ("\n".join((text.decode('UTF-8')).splitlines()))}]},
                                               headers={'X-Auth-Token': pasteToken})
                actual_link = paste_response.json()
                await channel_embed(message.channel, 'Contents uploaded to paste.ee', (actual_link["link"]))
                logging.info(f'{message.author.id} uploaded a paste to {(actual_link["link"])}')


async def gexre(message, b_discord, exempt_channels):
    try:
        member_check = b_discord.get_member(message.author.id)
        if b_discord.get_role(ignoreRole) not in member_check.roles:
            ignore = False
        else:
            ignore = True
    except AttributeError:
        ignore = False
    if (b_discord.get_member(bbi) in message.mentions) or (
            (ignore is False) and (str(message.channel.id) not in exempt_channels)):
        with open('./data/responses.json') as jsonResp:
            response_list = json.load(jsonResp)
        for x in range(1, (len(response_list) + 1)):
            if js_regex.compile(response_list[x - 1]['regex']).search(message.content):
                await channel_embed(message.channel, (response_list[x - 1]['title']),
                                    (response_list[x - 1]['description']))


class Messageon(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        await del_blacklist(message, b_discord=self.bot.get_guild(baritoneDiscord))

        channel = await self.bot.fetch_channel(logChannel)
        async for message in channel.history():
            if (message.created_at + timedelta(hours=24)) < datetime.utcnow():
                await message.delete()
                logging.info('cleared logs older then 24 hours in the logs channel')
        await self.bot.process_commands(message)


def setup(bot):
    bot.add_cog(Messageon(bot))
