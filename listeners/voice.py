import discord
from discord.ext import commands


class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(
        self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState
    ):
        voice_role = member.guild.get_role(self.bot.db.get_voice_role_id(member.guild.id))
        if before.channel is None and voice_role not in member.roles:
            return await member.add_roles(voice_role)
        if after.channel is None and voice_role in member.roles:
            return await member.remove_roles(voice_role)


async def setup(bot):
    await bot.add_cog(Voice(bot))
