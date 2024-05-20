import time
import logging

import discord
from discord.ext import commands

from utils import get_unix, slash_embed

log = logging.getLogger('commands.ping_command')


class RePing(discord.ui.View):
    def __init__(self, bot, timeout: int = None):
        super().__init__(timeout=timeout)
        self.bot = bot

    @discord.ui.button(label='Ping again!', emoji='🏓', style=discord.ButtonStyle.blurple, custom_id='ping')
    async def button_callback(self, inter: discord.Interaction, _button: discord.ui.Button):
        ms = get_unix(inter.id) - round(time.time() * 1000)

        await slash_embed(
            inter,
            inter.user,
            title=f'Pong! 🏓 ({abs(ms)}ms)',
            color=self.bot.db.get_embed_color(inter.guild.id),
            view=self,
            is_interaction=True
        )
        log.info(f'{inter.user.id} used the ping command with {ms}ms')


class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name='ping', description='da ping command')
    async def ping(self, inter: discord.Interaction):
        ms = (get_unix(inter.id)) - round(time.time() * 1000)

        await slash_embed(
            inter,
            inter.user,
            title=f'Pong! 🏓 ({abs(ms)}ms)',
            color=self.bot.db.get_embed_color(inter.guild.id),
            view=RePing(bot=self.bot)
        )
        log.info(f'{inter.user.id} used the ping command with {ms}ms')

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(RePing(bot=self.bot))


async def setup(bot):
    await bot.add_cog(Ping(bot))
