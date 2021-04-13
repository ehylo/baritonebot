import discord
import logging
import requests
from cogs.const import preCmd, logChannel, log_embed, exmChl, channel_embed, pasteToken, bbi
from datetime import datetime, timedelta
from discord.ext import commands

class Messageon(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild is None and message.author != self.bot.user: # log dms
            channel = await self.bot.fetch_channel(logChannel)
            title = (f'I have recieved a DM')
            desc = message.content
            ctx = message
            await log_embed(ctx, title, desc, channel)
            logging.info(f'{message.author.id} dmed me \"{message.content}\"')
        elif message.author.id != bbi and str(message.channel.id) not in exmChl: # deleting blacklisted words
            if message.content.startswith(f'{preCmd}blacklist add '):
                pass
            else:
                with open("./data/blacklist.txt", "r") as f:
                    lines = f.readlines()
                    res = [sub.replace('\n', '') for sub in lines]
                    for line in res:
                        if line in str(message.content):
                            await message.delete()
        if len(message.attachments) > 0: # log/json/txt file to paste for ease idk
            if message.attachments[0].url.lower().endswith(('.log', '.txt', '.json')):
                text = await discord.Attachment.read(message.attachments[0], use_cached=False)
                text = text.decode('UTF-8')
                text = "\n".join(text.splitlines())
                payload = {'sections':[{'name':"Paste from " + str(message.author),'contents': text}]}
                headers = {'X-Auth-Token': pasteToken}
                paste_response = requests.post(url='https://api.paste.ee/v1/pastes', json=payload, headers=headers)
                actual_link = paste_response.json()
                title= 'Contents uploaded to paste.ee'
                desc = (actual_link["link"])
                ctx = message.channel
                await channel_embed(ctx, title, desc)
                logging.info(f'{message.author.id} uploaded a paste to {(actual_link["link"])}')
        channel = await self.bot.fetch_channel(logChannel) # clearing logs
        async for message in channel.history():
            if (message.created_at + timedelta(hours = 24)) < datetime.utcnow():
                await message.delete()
                logging.info('cleared logs older then 24 hours in the logs channel')

def setup(bot):
    bot.add_cog(Messageon(bot))