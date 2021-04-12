import discord
import logging
from cogs.const import preCmd, logChannel, log_embed, exmChl
from datetime import datetime, timedelta
from discord.ext import commands

class Messageon(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        #log dms
        if message.guild is None and message.author != self.bot.user:
            channel = await self.bot.fetch_channel(logChannel)
            title = (f'I have recieved a DM')
            desc = message.content
            ctx = message
            await log_embed(ctx, title, desc, channel)
            logging.info(f'{message.author.id} dmed me \"{message.content}\"')
        #deleting blacklisted words
        elif message.author.id != (823620099054239744) and str(message.channel.id) not in exmChl:
            if f'{preCmd}blacklist add ' not in message.content:
                with open("./data/blacklist.txt", "r") as f:
                    lines = f.readlines()
                    res = [sub.replace('\n', '') for sub in lines]
                    for line in res:
                        if line in str(message.content):
                            await message.delete()
        #clearing logs
        channel = await self.bot.fetch_channel(logChannel)
        async for message in channel.history():
            if (message.created_at + timedelta(hours = 24)) < datetime.utcnow():
                await message.delete()
                logging.info('cleared logs older then 24 hours in the logs channel')

def setup(bot):
    bot.add_cog(Messageon(bot))