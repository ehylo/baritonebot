import logging

import discord
from discord.ext import commands

from utils import get_channel

log = logging.getLogger('listeners.edited_logger')


class EditedMessageJump(discord.ui.View):
    def __init__(self, url: str):
        super().__init__()
        self.url = url
        self.add_item(discord.ui.Button(label='Jump', url=url, style=discord.ButtonStyle.grey))


class EditedLogger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_edit(self, message_before: discord.Message, message_after: discord.Message):

        # ignore webhooks
        if message_after.author.discriminator == '0000':
            return
        # ignore blank before/afters (embeds)
        if message_after.content == '' or message_before.content == '':
            return
        # ignore messages from the bot
        if message_after.author.id == self.bot.db.bot_id:
            return
        # ignore messages that didn't change (buttons, interactions, etc.)
        if message_after.content == message_before.content:
            return
        # ignore dms
        if message_after.guild is None:
            return
        # ignore large messages that can't be embedded
        if len(message_before.content) > 1024 or len(message_after.content) > 1024:
            return
        # ignore exempted channels
        if message_after.channel.id in self.bot.db.get_exempt_channel_ids(message_after.guild.id):
            return

        # build the embed
        embed_var = discord.Embed(
            color=self.bot.db.get_embed_color(message_after.guild.id),
            description=f'**Message edited in {message_after.channel.mention}**'
        )
        embed_var.add_field(name='Before Edit:', value=message_before.content, inline=False)
        embed_var.add_field(name='After Edit:', value=message_after.content, inline=False)
        embed_var.set_footer(
            text=f'{message_after.author.name} | ID: {message_after.author.id}',
            icon_url=message_after.author.display_avatar.url
        )
        channel = await get_channel(self.bot, self.bot.db.get_logs_channel_id(message_after.guild.id))
        await channel.send(embed=embed_var, view=EditedMessageJump(message_after.jump_url))
        log.info(f'message edited in {message_after.channel.id}, '
                 f'before: {message_before.content}\n\nafter: {message_after.content}')


async def setup(bot):
    await bot.add_cog(EditedLogger(bot))
