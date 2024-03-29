from typing import Literal

import discord
from discord.ext import commands

from utils.embeds import slash_embed


class UndoAddIgnored(discord.ui.View):
    def __init__(self, bot, timeout: int = None):
        super().__init__(timeout=timeout)
        self.bot = bot

    @discord.ui.button(label='Undo', emoji='↪', style=discord.ButtonStyle.grey, custom_id='add_ignore')
    async def button_callback(self, inter: discord.Interaction, button: discord.ui.Button):
        button.disabled = True
        if inter.guild.get_role(self.bot.db.ignore_id[inter.guild.id]) not in inter.user.roles:
            return await slash_embed(
                inter, inter.user, 'You don\'t have the ignored role', view=self, is_interaction=True
            )
        await inter.user.remove_roles(inter.guild.get_role(self.bot.db.ignore_id[inter.guild.id]))
        await slash_embed(
            inter,
            inter.user,
            'Your messages will now trigger the response regexes.',
            'Ignored role removed',
            self.bot.db.embed_color[inter.guild.id],
            view=self,
            is_interaction=True
        )


class UndoRemoveIgnored(discord.ui.View):
    def __init__(self, bot, timeout: int = None):
        super().__init__(timeout=timeout)
        self.bot = bot

    @discord.ui.button(label='Undo', emoji='↪', style=discord.ButtonStyle.grey, custom_id='remove_ignore')
    async def button_callback(self, inter: discord.Interaction, button: discord.ui.Button):
        button.disabled = True
        if inter.guild.get_role(self.bot.db.ignore_id[inter.guild.id]) in inter.user.roles:
            return await slash_embed(inter, inter.user, 'You have the ignored role', view=self, is_interaction=True)
        await inter.user.add_roles(inter.guild.get_role(self.bot.db.ignore_id[inter.guild.id]))
        await slash_embed(
            inter,
            inter.user,
            'Your messages will now not trigger the response regexes unless you ping me.',
            'Ignored role added',
            self.bot.db.embed_color[inter.guild.id],
            view=self,
            is_interaction=True
        )


class Ignored(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(
        name='ignored',
        description='Add/remove the ignored role, if you have this you will not trigger most of the responses'
    )
    @discord.app_commands.describe(action='Add or remove the ignored role')
    async def ignored(self, inter: discord.Interaction, action: Literal['Add', 'Remove']):
        if action == 'Add':
            if inter.guild.get_role(self.bot.db.ignore_id[inter.guild.id]) in inter.user.roles:
                return await slash_embed(inter, inter.user, 'You already have the ignored role.')
            await inter.user.add_roles(inter.guild.get_role(self.bot.db.ignore_id[inter.guild.id]))
            await slash_embed(
                inter,
                inter.user,
                'Your messages will now not trigger the response regexes unless you ping me.',
                'Ignored role added',
                self.bot.db.embed_color[inter.guild.id],
                view=UndoAddIgnored(bot=self.bot)
            )
        if action == 'Remove':
            if inter.guild.get_role(self.bot.db.ignore_id[inter.guild.id]) not in inter.user.roles:
                return await slash_embed(inter, inter.user, 'You don\'t have the ignored role.')
            await inter.user.remove_roles(inter.guild.get_role(self.bot.db.ignore_id[inter.guild.id]))
            await slash_embed(
                inter,
                author=inter.user,
                title='Ignored role removed',
                description='Your messages will now trigger the response regexes.',
                color=self.bot.db.embed_color[inter.guild.id],
                view=UndoRemoveIgnored(bot=self.bot)
            )

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(UndoAddIgnored(bot=self.bot))
        self.bot.add_view(UndoRemoveIgnored(bot=self.bot))


async def setup(bot):
    await bot.add_cog(Ignored(bot))
