import discord
import logging
from discord.ext import commands
from cogs.const import coolEmbedColor, logChannel, leaveChannel, timeDate, log_embed, fault_footer

class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.id != (823620099054239744):
            title = None
            desc = (f'**Message deleted in <#{message.channel.id}>** \n{message.content}')
            ctx = message
            channel = await self.bot.fetch_channel(logChannel)
            await log_embed(ctx, title, desc, channel)
            logging.info(f'{message.author.id} message was deleted: \"{message.content}\"')

    @commands.Cog.listener()
    async def on_message_edit(self, message_before, message_after):
        if message_before.author.id != (823620099054239744):
            embedVar = discord.Embed(color = coolEmbedColor, timestamp=timeDate)
            embedVar.description =(f'**Message edited in <#{message_after.channel.id}>** [(jump)](https://discord.com/channels/{message_after.guild.id}/{message_after.channel.id}/{message_after.id})')
            embedVar.add_field(name='Befored Edit:', value=message_before.content, inline=True)
            embedVar.add_field(name='After Edit:', value=message_after.content, inline=True)
            embedVar.set_author(name=message_after.author, icon_url=message_after.author.avatar_url)
            embedVar.set_footer(text=(f'{fault_footer} ID: {message_after.author.id}'))
            channel = await self.bot.fetch_channel(logChannel)
            await channel.send(embed=embedVar)
            logging.info(f'{message_after.author.id} edited a message, Before:\"{message_before}\" After:\"{message_after}\"')

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        title=('User Left')
        desc = None
        ctx = None
        channel = await self.bot.fetch_channel(leaveChannel)
        await log_embed(ctx, title, desc, channel, member)
        logging.info(f'{member.id} left the server')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        title=('User Joined')
        desc = None
        ctx = None
        channel = await self.bot.fetch_channel(leaveChannel)
        await log_embed(ctx, title, desc, channel, member)
        logging.info(f'{member.id} joined the server')

def setup(bot):
    bot.add_cog(Logs(bot))