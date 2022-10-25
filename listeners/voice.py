import discord
from discord.ext import commands


class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(
        self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState
    ):
        if before.channel is None and member.guild.get_role(self.bot.db.voice_id[member.guild.id]) not in member.roles:
            return await member.add_roles(member.guild.get_role(self.bot.db.voice_id[member.guild.id]))
        if after.channel is None and member.guild.get_role(self.bot.db.voice_id[member.guild.id]) in member.roles:
            return await member.remove_roles(member.guild.get_role(self.bot.db.voice_id[member.guild.id]))


async def setup(bot):
    await bot.add_cog(Voice(bot))
