import time

import discord
from discord.commands import Option
from discord.ext import commands, tasks

from main import bot_db
from utils import embeds
from utils.misc import role_hierarchy, get_user
from utils.const import GUILD_ID


class Mute(commands.Cog):
    time_dict = {
        'Seconds': 1,
        'Minutes': 60,
        'Milidays (1/1000 of a Day)': 86,
        'Moments (90 Seconds)': 90,
        'Hours': 3600,
        'Days': 86400,
        'Weeks': 604800,
        'Mega Seconds (1mil Seconds)': 1000000,
        'Fortnights': 1209600,
        'Months': 2592000,
        'Quarantines (40 Days)': 3456000,
        'Semesters (18 Weeks)': 10886400,
        'Years': 31536000,
        'Gregorian Years (~Year)': 31556952,
        'Olympiads (4 Years)': 126144000,
        'Lustrums (5 Years)': 157680000,
        'Decades': 315360000,
        'Indictions (15 Years)': 473040000,
        'Giga Seconds (1bil Seconds)': 1000000000,
        'Jubilees (50 Years)': 1576800000,
        'Centuries': 3153600000,
        'Kiloannums/Millenniums': 31563000000,
        'Megaannums/Megayears (1mil Years)': 31536000000000,
        'Galactic Years (~230mil Years)': 7253280000000000,
        'Cosmological Decades (varies)': 10000000000000000
    }

    def __init__(self, bot):
        self.bot = bot
        self.loops.start()

    def cog_unload(self):
        self.loops.cancel()

    @tasks.loop(seconds=5)
    async def loops(self):
        for guild_id in bot_db.mutes:
            for user in bot_db.mutes[guild_id]:
                if user[1] <= time.time() and user[1] != 0:
                    guild = self.bot.get_guild(guild_id)
                    await guild.get_member(user[0]).remove_roles(guild.get_role(bot_db.muted_id[guild_id]))
                    new_mutes = bot_db.mutes[guild_id]
                    new_mutes.remove(user)
                    bot_db.update_mutes(guild, new_mutes)

    @loops.before_loop
    async def before_loops(self):
        await self.bot.wait_until_ready()

    @discord.slash_command(
        name='mute',
        description='mutes the specified member for the specified amount of time',
        guild_ids=[GUILD_ID]
    )
    @discord.default_permissions(view_audit_log=True)
    async def mute(
        self,
        ctx,
        offender: Option(discord.Member, name='member', description='Member you wish to mute', required=True),
        time_unit: Option(
            name='units',
            description='unit of time',
            choices=list(time_dict),
            required=True
        ),
        time_duration: Option(
            int,
            name='duration',
            description='duration for the units',
            required=True,
            min_value=1
        ),
        reason: Option(name='reason', description='The reason you are muting this member', required=True)
    ):
        time_text = f'{time_duration} {time_unit.lower()}'
        if time_duration * self.time_dict[time_unit] + time.time() > 9223372036854775800:
            expiry = 0
        else:
            expiry = time_duration * self.time_dict[time_unit] + time.time()
        if ctx.guild.get_role(bot_db.muted_id[ctx.guild.id]) in offender.roles:
            return await embeds.slash_embed(ctx, ctx.author, f'{offender.mention} is already muted!')
        if not role_hierarchy(bot_db, ctx.guild.id, enforcer=ctx.author, offender=offender):
            return await embeds.slash_embed(ctx, ctx.author, f'You don\'t outrank {offender.mention}')
        new_mutes = bot_db.mutes[ctx.guild.id]
        new_mutes.append([offender.id, expiry])
        bot_db.update_mutes(ctx.guild, new_mutes)
        await offender.add_roles(ctx.guild.get_role(bot_db.muted_id[ctx.guild.id]))
        await embeds.slash_embed(
            ctx,
            ctx.author,
            f'{offender.mention} has been muted for {time_text}, Reason: ```{reason}```', 'Member Muted',
            bot_db.embed_color[ctx.guild.id],
            False
        )
        await embeds.mod_log_embed(
            self.bot,
            bot_db,
            ctx.guild.id,
            author=ctx.author,
            offender=offender,
            title='Member Muted',
            description=f'{offender.mention} has been muted for {time_text}, Reason: ```{reason}```'
        )
        dm_channel = await offender.create_dm()
        await embeds.dm_embed(
            bot_db,
            ctx.guild.id,
            channel=dm_channel,
            author=ctx.author,
            title='Muted',
            description=f'You have been muted in the baritone discord for {time_text}, Reason: \n```{reason}```'
        )

    @discord.slash_command(name='unmute', description='un-mutes the specified member', guild_ids=[GUILD_ID])
    @discord.default_permissions(view_audit_log=True)
    async def unmute(
        self,
        ctx,
        offender: Option(discord.Member, name='member', description='Member you wish to un-mute', required=True)
    ):
        if not role_hierarchy(bot_db, ctx.guild.id, enforcer=ctx.author, offender=offender):
            return await embeds.slash_embed(ctx, ctx.author, f'You don\'t outrank {offender.mention}')
        if not ctx.guild.get_role(bot_db.muted_id[ctx.guild.id]) in offender.roles:
            return await embeds.slash_embed(ctx, ctx.author, f'{offender.mention} is not muted.')
        for mutes_list in bot_db.mutes[ctx.guild.id]:
            if mutes_list[0] == offender.id:
                new_mutes = bot_db.mutes[ctx.guild.id]
                new_mutes.remove(mutes_list)
                bot_db.update_mutes(ctx.guild, new_mutes)
                break
        await offender.remove_roles(ctx.guild.get_role(bot_db.muted_id[ctx.guild.id]))
        await embeds.slash_embed(
            ctx,
            ctx.author,
            f'{offender.mention} has been un-muted',
            'Member Un-Muted',
            bot_db.embed_color[ctx.guild.id],
            False
        )

    @discord.slash_command(name='mute-list', description='lists the current muted members', guild_ids=[GUILD_ID])
    @discord.default_permissions(view_audit_log=True)
    async def mute_list(self, ctx):
        description = ''
        for muted_user in bot_db.mutes[ctx.guild.id]:
            user = await get_user(self.bot, muted_user[0])
            remaining = 'indefinite' if muted_user[1] == 0 else f'<t:{int(muted_user[1])}:F>'
            description += f'**{user} ({user.id}) muted until:** \n{remaining}\n'
        await embeds.slash_embed(
            ctx,
            ctx.author,
            description,
            f'Muted Users ({len(bot_db.mutes[ctx.guild.id])})',
            bot_db.embed_color[ctx.guild.id],
            False
        )


def setup(bot):
    bot.add_cog(Mute(bot))
