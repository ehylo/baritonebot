import discord
from discord.ext import commands

from utils.const import HOISTED_CHARS


async def remove_hoist(hoisted_chars, member):

    def name_loop(name):
        if name.startswith(hoisted_chars):
            return name_loop(name[1:])
        if name == '':
            return 'z' + member.name
        return name
    await member.edit(nick=name_loop(member.display_name))


class AntiHoist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.name.startswith(HOISTED_CHARS):
            await remove_hoist(HOISTED_CHARS, member)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        try:
            if after.display_name.startswith(HOISTED_CHARS):
                if not before.display_name.startswith(HOISTED_CHARS):
                    return await after.edit(nick=before.display_name)
                await remove_hoist(HOISTED_CHARS, after)
        except discord.Forbidden:
            pass  # bot doesn't have permissions to change that member's nick


def setup(bot):
    bot.add_cog(AntiHoist(bot))
