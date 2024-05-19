import logging

import discord
from discord.ext import commands

from utils import HOISTED_CHARS

log = logging.getLogger('listeners.anti_hoist')


async def remove_hoist(hoisted_chars: tuple[str], member: discord.Member):

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
    async def on_member_join(self, member: discord.Member):
        if member.name.startswith(HOISTED_CHARS):
            log.info(f'{member.id} joined with a hoisted character, removing it')
            await remove_hoist(HOISTED_CHARS, member)

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        try:
            if after.display_name.startswith(HOISTED_CHARS):
                log.info(f'{after.id} edited their name to start with a hoisted character, removing it')
                if not before.display_name.startswith(HOISTED_CHARS):
                    return await after.edit(nick=before.display_name)
                await remove_hoist(HOISTED_CHARS, after)
        except discord.Forbidden:
            log.warning(f'tried to remove hoisted characters from {after.id} but I don\' have sufficient permissions')


async def setup(bot):
    await bot.add_cog(AntiHoist(bot))
