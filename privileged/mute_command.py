import enum
import time
import logging

import discord
from discord.ext import commands, tasks

from utils import role_hierarchy, get_user, slash_embed, mod_log_embed, dm_embed

log = logging.getLogger('privileged.mute_command')

time_dict = enum.Enum(
    value='time_dict',
    names=[
        ('Seconds', 1),
        ('Minutes', 60),
        ('Milidays (1/1000 of a Day)', 86),
        ('Moments (90 Seconds)', 90),
        ('Hours', 3600),
        ('Days', 86400),
        ('Weeks', 604800),
        ('Mega Seconds (1mil Seconds)', 1000000),
        ('Fortnights', 1209600),
        ('Months', 2592000),
        ('Quarantines (40 Days)', 3456000),
        ('Semesters (18 Weeks)', 10886400),
        ('Years', 31536000),
        ('Gregorian Years (~Year)', 31556952),
        ('Olympiads (4 Years)', 126144000),
        ('Lustrums (5 Years)', 157680000),
        ('Decades', 315360000),
        ('Indictions (15 Years)', 473040000),
        ('Giga Seconds (1bil Seconds)', 1000000000),
        ('Jubilees (50 Years)', 1576800000),
        ('Centuries', 3153600000),
        ('Kiloannums/Millenniums', 31563000000),
        ('Megaannums/Megayears (1mil Years)', 31536000000000),
        ('Galactic Years (~230mil Years)', 7253280000000000),
        ('Cosmological Decades (varies)', 9007199254740991)  # 10000000000000000
    ]
)


class Mute(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.loops.start()

    def cog_unload(self):
        self.loops.cancel()

    @tasks.loop(seconds=5)
    async def loops(self):
        for guild in self.bot.guilds:
            for user in self.bot.db.get_mutes(guild.id):
                if user['expiry'] <= time.time() and user['expiry'] != 0:
                    await guild.get_member(user['user_id']).remove_roles(
                        guild.get_role(self.bot.db.get_muted_role_id(guild.id))
                    )
                    await self.bot.db.delete_mute(guild.id, user['user_id'])
                    log.info(f'unmuted {user["user_id"]} from {guild.id}')

    @loops.before_loop
    async def before_loops(self):
        await self.bot.wait_until_ready()

    @discord.app_commands.command(description='mutes the specified member for the specified amount of time')
    @discord.app_commands.default_permissions(view_audit_log=True)
    @discord.app_commands.describe(
        offender='Member you wish to mute',
        time_unit='unit of time',
        time_duration='duration for the units',
        reason='The reason you are muting this member'
    )
    @discord.app_commands.rename(offender='member', time_unit='units', time_duration='duration')
    async def mute(
        self,
        inter: discord.Interaction,
        offender: discord.Member,
        time_unit: time_dict,
        time_duration: discord.app_commands.Range[int, 1],
        reason: str
    ):
        time_text = f'{time_duration} {time_unit.lower()}'
        if time_duration * time_unit.value + time.time() > 9223372036854775800:
            expiry = 0
        else:
            expiry = time_duration * time_unit.value + time.time()
        muted_role = inter.guild.get_role(self.bot.db.get_muted_role_id(inter.guild.id))
        if muted_role in offender.roles:
            return await slash_embed(inter, inter.user, f'{offender.mention} is already muted!')
        if not role_hierarchy(self.bot.db, inter.guild.id, enforcer=inter.user, offender=offender):
            return await slash_embed(inter, inter.user, f'You don\'t outrank {offender.mention}')
        await self.bot.db.new_mute(inter.guild.id, offender.id, expiry)
        await offender.add_roles(muted_role)
        await slash_embed(
            inter,
            inter.user,
            f'{offender.mention} has been muted for {time_text}, Reason: ```{reason}```',
            'Member Muted',
            self.bot.db.get_embed_color(inter.guild.id),
            False
        )
        await mod_log_embed(
            self.bot,
            self.bot.db,
            inter.guild.id,
            author=inter.user,
            offender=offender,
            title='Member Muted',
            description=f'{offender.mention} has been muted for {time_text}, Reason: ```{reason}```'
        )
        dm_channel = await offender.create_dm()
        await dm_embed(
            self.bot.db,
            inter.guild.id,
            channel=dm_channel,
            author=inter.user,
            title='Muted',
            description=f'You have been muted in the baritone discord for {time_text}, Reason: \n```{reason}```'
        )
        log.info(f'{inter.user.id} muted {offender.id} for {time_text} with reason: {reason}')

    @discord.app_commands.command(description='un-mutes the specified member')
    @discord.app_commands.default_permissions(view_audit_log=True)
    @discord.app_commands.rename(offender='member')
    @discord.app_commands.describe(offender='Member you wish to un-mute')
    async def unmute(self, inter: discord.Interaction, offender: discord.Member):
        if not role_hierarchy(self.bot.db, inter.guild.id, enforcer=inter.user, offender=offender):
            return await slash_embed(inter, inter.user, f'You don\'t outrank {offender.mention}')
        muted_role = inter.guild.get_role(self.bot.db.get_muted_role_id(inter.guild.id))
        if muted_role not in offender.roles:
            return await slash_embed(inter, inter.user, f'{offender.mention} is not muted.')
        for mutes_dict in self.bot.db.get_mutes(inter.guild.id):
            if mutes_dict['user_id'] == offender.id:
                await self.bot.db.delete_mute(inter.guild.id, offender.id)
                break
        await offender.remove_roles(muted_role)
        await slash_embed(
            inter,
            inter.user,
            f'{offender.mention} has been un-muted',
            'Member Un-Muted',
            self.bot.db.get_embed_color(inter.guild.id),
            False
        )
        log.info(f'{inter.user.id} unmuted {offender.id}')

    @discord.app_commands.command(name='mute-list', description='lists the current muted members')
    @discord.app_commands.default_permissions(view_audit_log=True)
    async def mute_list(self, inter: discord.Interaction):
        description = ''
        for muted_dict in self.bot.db.get_mutes(inter.guild.id):
            user = await get_user(self.bot, muted_dict['user_id'])
            remaining = 'indefinite' if muted_dict['expiry'] == 0 else f'<t:{int(muted_dict["expiry"])}:F>'
            description += f'**{user} ({user.id}) muted until:** \n{remaining}\n'
        await slash_embed(
            inter,
            inter.user,
            description,
            f'Muted Users ({len(self.bot.db.get_mutes(inter.guild.id))})',
            self.bot.db.get_embed_color(inter.guild.id),
            False
        )


async def setup(bot):
    await bot.add_cog(Mute(bot))
