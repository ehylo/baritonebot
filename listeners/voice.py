import logging

import discord
from discord.ext import commands

log = logging.getLogger('listeners.voice')


class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(
        self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState
    ):
        voice_role = member.guild.get_role(self.bot.db.get_voice_role_id(member.guild.id))

        # check if they just joined a voice channel
        if before.channel is None and voice_role not in member.roles:
            await member.add_roles(voice_role)
            log.info(f'{member.id} joined the voice channel {after.channel.id}')

        # check if they just left a voice channel
        if after.channel is None and voice_role in member.roles:
            await member.remove_roles(voice_role)
            log.info(f'{member.id} left the voice channel {before.channel.id}')


async def setup(bot):
    await bot.add_cog(Voice(bot))
