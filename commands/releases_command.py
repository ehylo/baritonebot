from typing import Literal

import discord
from discord.ext import commands

from utils import slash_embed


class UndoAddReleases(discord.ui.View):
    def __init__(self, bot, timeout: int = None):
        super().__init__(timeout=timeout)
        self.bot = bot

    @discord.ui.button(label='Undo', emoji='↪', style=discord.ButtonStyle.grey, custom_id='add_release')
    async def button_callback(self, inter: discord.Interaction, button: discord.ui.Button):
        button.disabled = True
        if inter.guild.get_role(self.bot.db.get_release_role_id(inter.guild.id)) not in inter.user.roles:
            return await slash_embed(
                inter, inter.user, 'You don\'t have the release role', view=self, is_interaction=True
            )
        await inter.user.remove_roles(inter.guild.get_role(self.bot.db.get_release_role_id(inter.guild.id)))
        await slash_embed(
            inter,
            inter.user,
            'You will not be pinged when a new release is made now.',
            'Releases role removed',
            self.bot.db.get_embed_color(inter.guild.id),
            view=self,
            is_interaction=True
        )


class UndoRemoveReleases(discord.ui.View):
    def __init__(self, bot, timeout: int = None):
        super().__init__(timeout=timeout)
        self.bot = bot

    @discord.ui.button(label='Undo', emoji='↪', style=discord.ButtonStyle.grey, custom_id='remove_release')
    async def button_callback(self, inter: discord.Interaction, button: discord.ui.Button):
        button.disabled = True
        if inter.guild.get_role(self.bot.db.get_release_role_id(inter.guild.id)) in inter.user.roles:
            return await slash_embed(inter, inter.user, 'You have the release role', view=self, is_interaction=True)
        await inter.user.add_roles(inter.guild.get_role(self.bot.db.get_release_role_id(inter.guild.id)))
        await slash_embed(
            inter,
            inter.user,
            'You will now be pinged when a new release is made!',
            'Releases role added',
            self.bot.db.get_embed_color(inter.guild.id),
            view=self,
            is_interaction=True
        )


class Releases(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(
        name='releases',
        description='Add/remove the releases role, if you have this you will be pinged when a new release comes out'
    )
    @discord.app_commands.describe(action='Add or remove the releases role')
    async def releases(self, inter: discord.Interaction, action: Literal['Add', 'Remove']):
        if action == 'Add':
            if inter.guild.get_role(self.bot.db.get_release_role_id(inter.guild.id)) in inter.user.roles:
                return await slash_embed(inter, inter.user, 'You already have the releases role.')
            await inter.user.add_roles(inter.guild.get_role(self.bot.db.get_release_role_id(inter.guild.id)))
            await slash_embed(
                inter,
                inter.user,
                'You will now be pinged when a new release is made!',
                'Releases role added',
                self.bot.db.get_embed_color(inter.guild.id),
                view=UndoAddReleases(bot=self.bot)
            )
        if action == 'Remove':
            if inter.guild.get_role(self.bot.db.get_release_role_id(inter.guild.id)) not in inter.user.roles:
                return await slash_embed(inter, inter.user, 'You don\'t have the releases role.')
            await inter.user.remove_roles(inter.guild.get_role(self.bot.db.get_release_role_id(inter.guild.id)))
            await slash_embed(
                inter,
                author=inter.user,
                title='Releases role removed',
                description='You will not be pinged when a new release is made now.',
                color=self.bot.db.get_embed_color(inter.guild.id),
                view=UndoRemoveReleases(bot=self.bot)
            )

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(UndoAddReleases(bot=self.bot))
        self.bot.add_view(UndoRemoveReleases(bot=self.bot))


async def setup(bot):
    await bot.add_cog(Releases(bot))
