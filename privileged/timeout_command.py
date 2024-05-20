from typing import Literal
from datetime import timedelta
import logging

import discord
from discord.ext import commands

from utils import role_hierarchy, TIME_KEYS, FOUR_WEEKS, dm_embed, mod_log_embed, slash_embed

log = logging.getLogger('privileged.timeout_command')


class TimeOut(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(
        name='timeout', description='timeouts the specified member for the specified amount of time'
    )
    @discord.app_commands.describe(
        offender='Member you wish to timeout',
        time_unit='unit of time',
        time_duration='duration for the units',
        reason='The reason you are timing out this member'
    )
    @discord.app_commands.rename(offender='member', time_unit='units', time_duration='duration')
    @discord.app_commands.default_permissions(view_audit_log=True)
    async def time_out(
        self,
        inter: discord.Interaction,
        offender: discord.Member,
        time_unit: Literal['Seconds', 'Minutes', 'Hours', 'Days', 'Weeks'],
        time_duration: discord.app_commands.Range[int, 1],
        reason: str
    ):
        time_text = f'{time_duration} {time_unit.lower()}'

        # timeouts have a max of four weeks, so we have to make sure it's in that range
        if TIME_KEYS[time_unit] * time_duration > FOUR_WEEKS:
            return await slash_embed(inter, inter.user, 'Discord only allows 4 weeks, please chose less.')

        # make sure that the person using the command is above the person they are taking action against
        if not role_hierarchy(self.bot.db, inter.guild.id, enforcer=inter.user, offender=offender):
            return await slash_embed(inter, inter.user, f'You don\'t outrank {offender.mention}')

        # apply the timeout and send the embeds
        await offender.timeout(timedelta(seconds=TIME_KEYS[time_unit] * time_duration), reason=reason)
        await slash_embed(
            inter,
            inter.user,
            f'{offender.mention} has been timed out for {time_text}, Reason: ```{reason}```', 'Member Timed Out',
            self.bot.db.get_embed_color(inter.guild.id),
            False
        )
        await mod_log_embed(
            self.bot,
            self.bot.db,
            inter.guild.id,
            author=inter.user,
            offender=offender,
            title='Member Timed Out',
            description=f'{offender.mention} has been timed out for {time_text}, Reason: ```{reason}```'
        )
        dm_channel = await offender.create_dm()
        await dm_embed(
            self.bot.db,
            inter.guild.id,
            channel=dm_channel,
            author=inter.user,
            title='Timed Out',
            description=f'You have been timed out in the baritone discord for {time_text}, Reason: \n```{reason}```'
        )
        log.info(f'{inter.user.id} timed out {offender.id} for {time_text} with reason {reason}')

    @discord.app_commands.command(name='un-timeout', description='removes the timeout on the specified member')
    @discord.app_commands.describe(offender='Member you wish to un-timeout')
    @discord.app_commands.rename(offender='member')
    @discord.app_commands.default_permissions(view_audit_log=True)
    async def un_time_out(self, inter: discord.Interaction, offender: discord.Member):

        # make sure that the person using the command is above the person they are taking action against
        if not role_hierarchy(self.bot.db, inter.guild.id, enforcer=inter.user, offender=offender):
            return await slash_embed(inter, inter.user, f'You don\'t outrank {offender.mention}')

        # make sure they actually have a timeout applied
        if not offender.timed_out_until:
            return await slash_embed(inter, inter.user, f'{offender.mention} is not timed out.')

        await offender.timeout(None)
        await slash_embed(
            inter,
            inter.user,
            f'{offender.mention} has been un-timed-out',
            'Member Un-Timed-Out',
            self.bot.db.get_embed_color(inter.guild.id),
            False
        )
        log.info(f'{inter.user.id} removed the timeout from {offender.id}')


async def setup(bot):
    await bot.add_cog(TimeOut(bot))
