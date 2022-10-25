from typing import Literal
from datetime import timedelta

import discord
from discord.ext import commands

from utils.misc import role_hierarchy
from utils.const import TIME_KEYS, FOUR_WEEKS
from utils import embeds


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
        if TIME_KEYS[time_unit] * time_duration > FOUR_WEEKS:
            return await embeds.slash_embed(inter, inter.user, 'Discord only allows 4 weeks, please chose less.')
        if not role_hierarchy(self.bot.db, inter.guild.id, enforcer=inter.user, offender=offender):
            return await embeds.slash_embed(inter, inter.user, f'You don\'t outrank {offender.mention}')
        await offender.timeout(timedelta(seconds=TIME_KEYS[time_unit] * time_duration), reason=reason)
        await embeds.slash_embed(
            inter,
            inter.user,
            f'{offender.mention} has been timed out for {time_text}, Reason: ```{reason}```', 'Member Timed Out',
            self.bot.db.embed_color[inter.guild.id],
            False
        )
        await embeds.mod_log_embed(
            self.bot,
            self.bot.db,
            inter.guild.id,
            author=inter.user,
            offender=offender,
            title='Member Timed Out',
            description=f'{offender.mention} has been timed out for {time_text}, Reason: ```{reason}```'
        )
        dm_channel = await offender.create_dm()
        await embeds.dm_embed(
            self.bot.db,
            inter.guild.id,
            channel=dm_channel,
            author=inter.user,
            title='Timed Out',
            description=f'You have been timed out in the baritone discord for {time_text}, Reason: \n```{reason}```'
        )

    @discord.app_commands.command(name='un-timeout', description='removes the timeout on the specified member')
    @discord.app_commands.describe(offender='Member you wish to un-timeout')
    @discord.app_commands.rename(offender='member')
    @discord.app_commands.default_permissions(view_audit_log=True)
    async def un_time_out(self, inter: discord.Interaction, offender: discord.Member):
        if not role_hierarchy(self.bot.db, inter.guild.id, enforcer=inter.user, offender=offender):
            return await embeds.slash_embed(inter, inter.user, f'You don\'t outrank {offender.mention}')
        if not offender.timed_out_until:
            return await embeds.slash_embed(inter, inter.user, f'{offender.mention} is not timed out.')
        await offender.timeout(None)
        await embeds.slash_embed(
            inter,
            inter.user,
            f'{offender.mention} has been un-timed-out',
            'Member Un-Timed-Out',
            self.bot.db.embed_color[inter.guild.id],
            False
        )


async def setup(bot):
    await bot.add_cog(TimeOut(bot))
