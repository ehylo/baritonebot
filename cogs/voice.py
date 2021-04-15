import discord
import logging
from discord.ext import commands
from cogs.const import voiceRole


class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member):
        if member.voice is not None:
            b_role = discord.utils.get(member.guild.roles, id=voiceRole)
            await member.add_roles(b_role)
            logging.info(f'{member.id} joined a voice channel and got the voice role')
        else:
            b_role = discord.utils.get(member.guild.roles, id=voiceRole)
            await member.remove_roles(b_role)
            logging.info(f'{member.id} left a voice channel and the voice role was removed')


def setup(bot):
    bot.add_cog(Voice(bot))
