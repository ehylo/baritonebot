import discord
import logging
from discord.ext import commands
from cogs.const import coolEmbedColor, logChannel, leaveChannel, timeDate, log_embed, fault_footer, bbi, error_embed


class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.id != bbi:
            channel = await self.bot.fetch_channel(logChannel)
            await log_embed(message, None, f'**Message deleted in <#{message.channel.id}>** \n{message.content}', channel)
            logging.info(f'{message.author.id} message was deleted: \"{message.content}\"')

    @commands.Cog.listener()
    async def on_message_edit(self, message_before, message_after):
        e_c = open("./data/exemptchannels.txt", "r")
        exempt_channels = e_c.read()
        e_c.close()
        if message_before.author.id != bbi and message_before.channel.id not in exempt_channels:
            embed = discord.Embed(color=coolEmbedColor, timestamp=timeDate, description=f'**Message edited in <#{message_after.channel.id}>** [(jump)](https://discord.com/channels/{message_after.guild.id}/{message_after.channel.id}/{message_after.id})')
            embed.add_field(name='Befored Edit:', value=message_before.content, inline=True)
            embed.add_field(name='After Edit:', value=message_after.content, inline=True)
            embed.set_author(name=message_after.author, icon_url=message_after.author.avatar_url)
            embed.set_footer(text=f'{fault_footer} ID: {message_after.author.id}')
            channel = await self.bot.fetch_channel(logChannel)
            await channel.send(embed=embed)
            logging.info(f'{message_after.author.id} edited a message, Before: \"{message_before.content}\" After: \"{message_after.content}\"')

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = await self.bot.fetch_channel(leaveChannel)
        await log_embed(None, 'User Left', None, channel, member)
        logging.info(f'{member.id} left the server')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = await self.bot.fetch_channel(leaveChannel)
        await log_embed(None, 'User Joined', None, channel, member)
        logging.info(f'{member.id} joined the server')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await error_embed(ctx, 'You need to give a **number**')
        elif isinstance(error, commands.errors.MemberNotFound):
            await error_embed(ctx, 'That member is invalid')
        elif not isinstance(error, commands.errors.CheckFailure):
            await error_embed(ctx, None, error)
            logging.error(f'{ctx.author.id} tried to use the command {ctx.command} but it gave the error: {error}')


def setup(bot):
    bot.add_cog(Logs(bot))
