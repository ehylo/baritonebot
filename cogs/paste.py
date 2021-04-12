import discord
import mimetypes
import requests
import logging
from discord.ext import commands
from cogs.const import pasteToken, channel_embed

class Paste(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if len(message.attachments) > 0:
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
                ctx = message
                await channel_embed(ctx, title, desc)
                logging.info(f'{ctx.author.id} uploaded a paste to {(actual_link["link"])}')

def setup(bot):
    bot.add_cog(Paste(bot))