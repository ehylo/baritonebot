import logging

import discord
from discord.ext import commands

from utils import HOISTED_CHARS

log = logging.getLogger('listeners.anti_hoist')


async def remove_hoist(hoisted_chars: tuple[str], member: discord.Member):

    def name_loop(name):

        # recursivley remove the characters until either there is no name left or the hoisted characters are all gone
        if name.startswith(hoisted_chars):
            return name_loop(name[1:])

        # if the name is fully removed, just add a z to the front
        if name == '':
            return 'z' + member.name

        return name

    # edit the users nickname
    await member.edit(nick=name_loop(member.display_name))


class AntiHoist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        try:
            if member.name.startswith(HOISTED_CHARS):
                await remove_hoist(HOISTED_CHARS, member)
                log.info(f'{member.id} joined with a hoisted character, removing it')

        except discord.Forbidden:  # make sure we actually have the permissions
            log.warning(f'tried to remove hoisted characters from {after.id} but I don\' have sufficient permissions')

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        try:
            if after.display_name.startswith(HOISTED_CHARS):

                # if the before is already in compliance, then just revert it
                if not before.display_name.startswith(HOISTED_CHARS):
                    return await after.edit(nick=before.display_name)

                # otherwise use our recursive function
                await remove_hoist(HOISTED_CHARS, after)
                log.info(f'{after.id} edited their name to start with a hoisted character, removing it')

        except discord.Forbidden:  # make sure we actually have the permissions
            log.warning(f'tried to remove hoisted characters from {after.id} but I don\' have sufficient permissions')


async def setup(bot):
    await bot.add_cog(AntiHoist(bot))
