from typing import Literal

import discord
from discord.ext import commands

from utils.embeds import slash_embed
from utils.misc import get_channel


class UndoAddExempt(discord.ui.View):
    def __init__(self, bot, timeout: int = None):
        super().__init__(timeout=timeout)
        self.bot = bot

    @discord.ui.button(label='Undo', emoji='↪', style=discord.ButtonStyle.grey, custom_id='add_exempt')
    async def button_callback(self, inter: discord.Interaction, button: discord.ui.Button):
        button.disabled = True
        exempt_list = self.bot.db.exempted_ids[inter.guild.id]
        channel = await get_channel(
            self.bot,
            int(inter.message.embeds[0].description.split(' will')[0].split('in ')[1][2:-1])
        )
        if channel.id not in self.bot.db.exempted_ids[inter.guild.id]:
            return await slash_embed(inter, inter.user, 'That channel isn\'t exempted', view=self, is_interaction=True)
        exempt_list.remove(channel.id)
        await self.bot.db.update_exempted_ids(inter.guild, exempt_list)
        await slash_embed(
            inter,
            inter.user,
            f'Edited/deleted messages in {channel.mention} will now be logged',
            'Channel un-exempted',
            self.bot.db.embed_color[inter.guild.id],
            view=self,
            is_interaction=True
        )


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
        if channel.id in self.bot.db.exempted_ids[inter.guild.id]:
            return await slash_embed(
                inter, inter.user, 'That channel is exempted already', view=self, is_interaction=True
            )
        await self.bot.db.update_exempted_ids(inter.guild, self.bot.db.exempted_ids[inter.guild.id] + [channel.id])
        await slash_embed(
            inter,
            inter.user,
            f'Edited/deleted messages in {channel.mention} will no longer be logged',
            'Channel exempted',
            self.bot.db.embed_color[inter.guild.id],
            view=self,
            is_interaction=True
        )


class Exempt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(description='exempts a channel from logging')
    @discord.app_commands.default_permissions(administrator=True)
    @discord.app_commands.describe(
        action='Add or remove a channel from the exempt list', channel='channel to remove or add from the exempt list'
    )
    async def exempt(self, inter: discord.Interaction, action: Literal['Add', 'Remove'], channel: discord.TextChannel):
        if action == 'Add':
            if channel.id in self.bot.db.exempted_ids[inter.guild.id]:
                return await slash_embed(inter, inter.user, 'That channel is exempted already')
            await self.bot.db.update_exempted_ids(inter.guild, self.bot.db.exempted_ids[inter.guild.id] + [channel.id])
            await slash_embed(
                inter,
                inter.user,
                f'Edited/deleted messages in {channel.mention} will no longer be logged',
                'Channel exempted',
                self.bot.db.embed_color[inter.guild.id],
                view=UndoAddExempt(bot=self.bot)
            )
        if action == 'Remove':
            if channel.id not in self.bot.db.exempted_ids[inter.guild.id]:
                return await slash_embed(inter, inter.user, 'That channel isn\'t exempted')
            exempt_list = self.bot.db.exempted_ids[inter.guild.id]
            exempt_list.remove(channel.id)
            await self.bot.db.update_exempted_ids(inter.guild, exempt_list)
            await slash_embed(
                inter,
                inter.user,
                f'Edited/deleted messages in {channel.mention} will now be logged',
                'Channel un-exempted',
                self.bot.db.embed_color[inter.guild.id],
                view=UndoRemoveExempt(bot=self.bot)
            )

    @discord.app_commands.command(name='exempt-list', description='lists the exempted/un-exempted channels')
    @discord.app_commands.default_permissions(administrator=True)
    @discord.app_commands.describe(action='List the exempted or un-exempted channels')
    @discord.app_commands.rename(action='option')
    async def exempt_list(self, inter: discord.Interaction, action: Literal['Exempted', 'Un-Exempted']):
        if action == 'Exempted':
            await slash_embed(
                inter,
                inter.user,
                f'<#{(">, <#".join(str(v) for v in self.bot.db.exempted_ids[inter.guild.id]))}>',
                f'Exempted Channels ({len(self.bot.db.exempted_ids[inter.guild.id])})',
                self.bot.db.embed_color[inter.guild.id]
            )
        if action == 'Un-Exempted':
            exempted_chl = self.bot.db.exempted_ids[inter.guild.id]
            channel_list = []
            for channel in inter.guild.text_channels:
                if channel.id not in exempted_chl:
                    channel_list.append(str(channel.id))
            await slash_embed(
                inter,
                inter.user,
                f'<#{(">, <#".join(channel_list))}>',
                f'Un-Exempted Channels ({len(channel_list)})',
                self.bot.db.embed_color[inter.guild.id]
            )

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(UndoAddExempt(bot=self.bot))
        self.bot.add_view(UndoRemoveExempt(bot=self.bot))


async def setup(bot):
    await bot.add_cog(Exempt(bot))
