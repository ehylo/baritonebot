from datetime import timedelta

import discord
from discord.commands import permissions, Option
from discord.ext import commands

from main import bot_db
from utils.misc import role_hierarchy
from utils.const import GUILD_ID, TIME_KEYS, FOUR_WEEKS
from utils import embeds


class TimeOut(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(
        name='timeout',
        description='timeouts the specified member for the specified amount of time',
        guild_ids=[GUILD_ID],
        default_permissions=False
    )
    @permissions.has_any_role(*sum((bot_db.helper_ids | bot_db.mod_ids | bot_db.admin_ids).values(), []))
    async def time_out(
        self,
        ctx,
        offender: Option(discord.Member, name='member', description='Member you wish to timeout', required=True),
        time_unit: Option(
            str,
            name='units',
            description='unit of time',
            choices=['Seconds', 'Minutes', 'Hours', 'Days', 'Weeks'],
            required=True
        ),
        time_duration: Option(
            int,
            name='duration',
            description='duration for the units',
            required=True,
            min_value=1
        ),
        reason: Option(str, name='reason', description='The reason you are timing out this member', required=True)
    ):
        time_text = f'{time_duration} {time_unit.lower()}'
        if TIME_KEYS[time_unit] * time_duration > FOUR_WEEKS:
            return await embeds.slash_embed(ctx, ctx.author, 'Discord only allows 4 weeks, please chose less.')
        if not role_hierarchy(bot_db, ctx.guild.id, enforcer=ctx.author, offender=offender):
            return await embeds.slash_embed(ctx, ctx.author, f'You don\'t outrank {offender.mention}')
        await offender.timeout_for(timedelta(seconds=TIME_KEYS[time_unit] * time_duration), reason=reason)
        await embeds.slash_embed(
            ctx,
            ctx.author,
            f'{offender.mention} has been timed out for {time_text}, Reason: ```{reason}```', 'Member Timed Out',
            bot_db.embed_color[ctx.guild.id],
            False
        )
        await embeds.mod_log_embed(
            self.bot,
            bot_db,
            ctx.guild.id,
            author=ctx.author,
            offender=offender,
            title='Member Timed Out',
            description=f'{offender.mention} has been timed out for {time_text}, Reason: ```{reason}```'
        )
        dm_channel = await offender.create_dm()
        await embeds.dm_embed(
            bot_db,
            ctx.guild.id,
            channel=dm_channel,
            author=ctx.author,
            title='Timed Out',
            description=f'You have been timed out in the baritone discord for {time_text}, Reason: \n```{reason}```'
        )

    @discord.slash_command(
        name='un-timeout',
        description='removes the timeout on the specified member',
        guild_ids=[GUILD_ID],
        default_permissions=False
    )
    @permissions.has_any_role(*sum((bot_db.helper_ids | bot_db.mod_ids | bot_db.admin_ids).values(), []))
    async def un_time_out(
        self,
        ctx,
        offender: Option(discord.Member, name='member', description='Member you wish to un-timeout', required=True)
    ):
        if not role_hierarchy(bot_db, ctx.guild.id, enforcer=ctx.author, offender=offender):
            return await embeds.slash_embed(ctx, ctx.author, f'You don\'t outrank {offender.mention}')
        if offender.timed_out is None:
            return await embeds.slash_embed(ctx, ctx.author, f'{offender.mention} is not timed out.')
        await offender.timeout(None)
        await embeds.slash_embed(
            ctx,
            ctx.author,
            f'{offender.mention} has been un-timed-out', 'Member Un-Timed-Out',
            bot_db.embed_color[ctx.guild.id],
            False
        )

    @discord.slash_command(
        name='timeout-list',
        description='lists the current timed-out members',
        guild_ids=[GUILD_ID],
        default_permissions=False
    )
    @permissions.has_any_role(*sum((bot_db.helper_ids | bot_db.mod_ids | bot_db.admin_ids).values(), []))
    async def timeout_list(self, ctx):
        pass


def setup(bot):
    bot.add_cog(TimeOut(bot))
