import logging

import discord
from discord.ext import commands

from utils import get_channel, get_unix

log = logging.getLogger('listeners.deleted_logger')


class DeletedLogger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload: discord.RawMessageDeleteEvent):
        log_channel = await get_channel(self.bot, self.bot.db.get_logs_channel_id(payload.guild_id))
        if log_channel.id == payload.channel_id:
            return
        if payload.cached_message is None:
            unix_time = get_unix(payload.message_id) // 1000
            embed_var = discord.Embed(
                color=self.bot.db.get_embed_color(payload.guild_id),
                description=f'Un-cached message deleted in <#{payload.channel_id}>, it was sent on <t:{unix_time}:F>'
            )
            log.info(f'uncached message deleted from {payload.channel_id} which was sent on {unix_time}')
            return await log_channel.send(embed=embed_var)
        message = payload.cached_message
        if message.author.discriminator == '0000':
            return
        if message.guild is None:
            return
        if message.channel.id in self.bot.db.get_exempt_channel_ids(message.guild.id):
            return

        # can't delete logged messages :)
        content = message.content if len(message.embeds) == 0 else message.embeds[0].description

        embed_var = discord.Embed(
            color=self.bot.db.get_embed_color(message.guild.id),
            description=f'**Message deleted in {message.channel.mention}**\n{content}'
        )
        embed_var.set_footer(
            text=f'{message.author.name} | ID: {message.author.id}',
            icon_url=message.author.display_avatar.url
        )
        log.info(f'message deleted in {message.channel.id}, content: {message.content}')
        await log_channel.send(embed=embed_var)


async def setup(bot):
    await bot.add_cog(DeletedLogger(bot))
