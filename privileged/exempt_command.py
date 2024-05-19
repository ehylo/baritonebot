from typing import Literal
import logging

import discord
from discord.ext import commands

from utils import slash_embed, get_channel

log = logging.getLogger('privileged.exempt_command')


class UndoAddExempt(discord.ui.View):
    def __init__(self, bot, timeout: int = None):
        super().__init__(timeout=timeout)
        self.bot = bot

    @discord.ui.button(label='Undo', emoji='↪', style=discord.ButtonStyle.grey, custom_id='add_exempt')
    async def button_callback(self, inter: discord.Interaction, button: discord.ui.Button):
        button.disabled = True
        channel = await get_channel(
            self.bot,
            int(inter.message.embeds[0].description.split(' will')[0].split('in ')[1][2:-1])
        )
        if channel.id not in self.bot.db.get_exempt_channel_ids(inter.guild.id):
            return await slash_embed(inter, inter.user, 'That channel isn\'t exempted', view=self, is_interaction=True)
        await self.bot.db.delete_exempted_id(inter.guild, channel.id)
        await slash_embed(
            inter,
            inter.user,
            f'Edited/deleted messages in {channel.mention} will now be logged',
            'Channel un-exempted',
            self.bot.db.get_embed_color(inter.guild.id),
            view=self,
            is_interaction=True
        )
        log.info(f'{inter.user.id} has removed the channel {channel.id} from the exempt list')


class UndoRemoveExempt(discord.ui.View):
    def __init__(self, bot, timeout: int = None):
        super().__init__(timeout=timeout)
        self.bot = bot

    @discord.ui.button(label='Undo', emoji='↪', style=discord.ButtonStyle.grey, custom_id='remove_exempt')
    async def button_callback(self, inter: discord.Interaction, button: discord.ui.Button):
        button.disabled = True
        channel = await get_channel(
            self.bot,
            int(inter.message.embeds[0].description.split(' will')[0].split('in ')[1][2:-1])
        )
        if channel.id in self.bot.db.get_exempt_channel_ids(inter.guild.id):
            return await slash_embed(
                inter, inter.user, 'That channel is exempted already', view=self, is_interaction=True
            )
        await self.bot.db.new_exempted_id(inter.guild.id, channel.id)
        await slash_embed(
            inter,
            inter.user,
            f'Edited/deleted messages in {channel.mention} will no longer be logged',
            'Channel exempted',
            self.bot.db.get_embed_color(inter.guild.id),
            view=self,
            is_interaction=True
        )
        log.info(f'{inter.user.id} has added the channel {channel.id} to the exempt list')


class Exempt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(description='exempts a channel from logging')
    @discord.app_commands.default_permissions(administrator=True)
    @discord.app_commands.describe(
        action='Add or remove a channel from the exempt list', channel='channel to remove or add from the exempt list'
    )
    async def exempt(self, inter: discord.Interaction, action: Literal['Add', 'Remove'], channel: discord.TextChannel):
        exempted_channel_ids = self.bot.db.get_exempt_channel_ids(inter.guild.id)
        if action == 'Add':
            if channel.id in exempted_channel_ids:
                return await slash_embed(inter, inter.user, 'That channel is exempted already')
            await self.bot.db.new_exempted_id(inter.guild.id, channel.id)
            await slash_embed(
                inter,
                inter.user,
                f'Edited/deleted messages in {channel.mention} will no longer be logged',
                'Channel exempted',
                self.bot.db.get_embed_color(inter.guild.id),
                view=UndoAddExempt(bot=self.bot)
            )
            log.info(f'{inter.user.id} has added the channel {channel.id} to the exempt list')
        if action == 'Remove':
            if channel.id not in exempted_channel_ids:
                return await slash_embed(inter, inter.user, 'That channel isn\'t exempted')
            await self.bot.db.delete_exempted_id(inter.guild.id, channel.id)
            await slash_embed(
                inter,
                inter.user,
                f'Edited/deleted messages in {channel.mention} will now be logged',
                'Channel un-exempted',
                self.bot.db.get_embed_color(inter.guild.id),
                view=UndoRemoveExempt(bot=self.bot)
            )
            log.info(f'{inter.user.id} has removed the channel {channel.id} from the exempt list')

    @discord.app_commands.command(name='exempt-list', description='lists the exempted/un-exempted channels')
    @discord.app_commands.default_permissions(administrator=True)
    @discord.app_commands.describe(action='List the exempted or un-exempted channels')
    @discord.app_commands.rename(action='option')
    async def exempt_list(self, inter: discord.Interaction, action: Literal['Exempted', 'Un-Exempted']):
        exempted_channel_ids = self.bot.db.get_exempt_channel_ids(inter.guild.id)
        if action == 'Exempted':
            await slash_embed(
                inter,
                inter.user,
                f'<#{(">, <#".join(str(v) for v in exempted_channel_ids))}>',
                f'Exempted Channels ({len(exempted_channel_ids)})',
                self.bot.db.get_embed_color(inter.guild.id)
            )
        if action == 'Un-Exempted':
            exempted_chls = exempted_channel_ids
            channel_list = []
            for channel in inter.guild.text_channels:
                if channel.id not in exempted_chls:
                    channel_list.append(str(channel.id))
            await slash_embed(
                inter,
                inter.user,
                f'<#{(">, <#".join(channel_list))}>',
                f'Un-Exempted Channels ({len(channel_list)})',
                self.bot.db.get_embed_color(inter.guild.id)
            )

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(UndoAddExempt(bot=self.bot))
        self.bot.add_view(UndoRemoveExempt(bot=self.bot))


async def setup(bot):
    await bot.add_cog(Exempt(bot))
