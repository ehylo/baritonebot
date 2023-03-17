import enum
import time

import discord
from discord.ext import commands, tasks

from utils import embeds
from utils.misc import role_hierarchy, get_user

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
        for guild_id in self.bot.db.mutes:
            for user in self.bot.db.mutes[guild_id]:
                if user[1] <= time.time() and user[1] != 0:
                    guild = self.bot.get_guild(guild_id)
                    await guild.get_member(user[0]).remove_roles(guild.get_role(self.bot.db.muted_id[guild_id]))
                    new_mutes = self.bot.db.mutes[guild_id]
                    new_mutes.remove(user)
                    await self.bot.db.update_mutes(guild, new_mutes)

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
        if inter.guild.get_role(self.bot.db.muted_id[inter.guild.id]) in offender.roles:
            return await embeds.slash_embed(inter, inter.user, f'{offender.mention} is already muted!')
        if not role_hierarchy(self.bot.db, inter.guild.id, enforcer=inter.user, offender=offender):
            return await embeds.slash_embed(inter, inter.user, f'You don\'t outrank {offender.mention}')
        new_mutes = self.bot.db.mutes[inter.guild.id]
        new_mutes.append([offender.id, expiry])
        await self.bot.db.update_mutes(inter.guild, new_mutes)
        await offender.add_roles(inter.guild.get_role(self.bot.db.muted_id[inter.guild.id]))
        await embeds.slash_embed(
            inter,
            inter.user,
            f'{offender.mention} has been muted for {time_text}, Reason: ```{reason}```', 'Member Muted',
            self.bot.db.embed_color[inter.guild.id],
            False
        )
        await embeds.mod_log_embed(
            self.bot,
            self.bot.db,
            inter.guild.id,
            author=inter.user,
            offender=offender,
            title='Member Muted',
            description=f'{offender.mention} has been muted for {time_text}, Reason: ```{reason}```'
        )
        dm_channel = await offender.create_dm()
        await embeds.dm_embed(
            self.bot.db,
            inter.guild.id,
            channel=dm_channel,
            author=inter.user,
            title='Muted',
            description=f'You have been muted in the baritone discord for {time_text}, Reason: \n```{reason}```'
        )

    @discord.app_commands.command(description='un-mutes the specified member')
    @discord.app_commands.default_permissions(view_audit_log=True)
    @discord.app_commands.rename(offender='member')
    @discord.app_commands.describe(offender='Member you wish to un-mute')
    async def unmute(self, inter: discord.Interaction, offender: discord.Member):
        if not role_hierarchy(self.bot.db, inter.guild.id, enforcer=inter.user, offender=offender):
            return await embeds.slash_embed(inter, inter.user, f'You don\'t outrank {offender.mention}')
        if not inter.guild.get_role(self.bot.db.muted_id[inter.guild.id]) in offender.roles:
            return await embeds.slash_embed(inter, inter.user, f'{offender.mention} is not muted.')
        for mutes_list in self.bot.db.mutes[inter.guild.id]:
            if mutes_list[0] == offender.id:
                new_mutes = self.bot.db.mutes[inter.guild.id]
                new_mutes.remove(mutes_list)
                await self.bot.db.update_mutes(inter.guild, new_mutes)
                break
        await offender.remove_roles(inter.guild.get_role(self.bot.db.muted_id[inter.guild.id]))
        await embeds.slash_embed(
            inter,
            inter.user,
            f'{offender.mention} has been un-muted',
            'Member Un-Muted',
            self.bot.db.embed_color[inter.guild.id],
            False
        )

    @discord.app_commands.command(name='mute-list', description='lists the current muted members')
    @discord.app_commands.default_permissions(view_audit_log=True)
    async def mute_list(self, inter: discord.Interaction):
        description = ''
        for muted_user in self.bot.db.mutes[inter.guild.id]:
            user = await get_user(self.bot, muted_user[0])
            remaining = 'indefinite' if muted_user[1] == 0 else f'<t:{int(muted_user[1])}:F>'
            description += f'**{user} ({user.id}) muted until:** \n{remaining}\n'
        await embeds.slash_embed(
            inter,
            inter.user,
            description,
            f'Muted Users ({len(self.bot.db.mutes[inter.guild.id])})',
            self.bot.db.embed_color[inter.guild.id],
            False
        )


async def setup(bot):
    await bot.add_cog(Mute(bot))
