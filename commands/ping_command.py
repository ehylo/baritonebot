import time

import discord
from discord.ext import commands

from main import bot_db
from utils.const import GUILD_ID
from utils.misc import get_unix
from utils.embeds import slash_embed


class RePing(discord.ui.View):
    @discord.ui.button(label='Ping again!', emoji='🏓', style=discord.ButtonStyle.blurple, custom_id='ping')
    async def button_callback(self, _: discord.ui.Button, inter):
        ms = get_unix(inter.id) - round(time.time() * 1000)
        await slash_embed(
            inter,
            inter.user,
            title=f'Pong! 🏓 ({ms}ms)',
            color=bot_db.embed_color[inter.guild.id],
            view=self,
            interaction=True
        )


class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name='ping', description='da ping command', guild_ids=[GUILD_ID])
    async def ping(self, ctx):
        ms = get_unix(ctx.interaction.id) - round(time.time() * 1000)
        await slash_embed(
            ctx,
            ctx.author,
            title=f'Pong! 🏓 ({ms}ms)',
            color=bot_db.embed_color[ctx.guild.id],
            view=RePing(timeout=None)
        )

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(RePing(timeout=None))


def setup(bot):
    bot.add_cog(Ping(bot))
