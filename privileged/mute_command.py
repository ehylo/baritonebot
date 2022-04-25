import discord
from discord.commands import permissions, Option
from discord.ext import commands

from main import bot_db
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

    @discord.slash_command(
        name='mute',
        description='mutes the specified member for the specified amount of time',
        guild_ids=[GUILD_ID],
        default_permissions=False
    )
    @permissions.has_any_role(*sum((bot_db.helper_ids | bot_db.mod_ids | bot_db.admin_ids).values(), []))
    async def mute(
        self,
        ctx,
        offender: Option(discord.Member, name='member', description='Member you wish to mute', required=True),
        time_unit: Option(
            str,
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
        reason: Option(str, name='reason', description='The reason you are muting this member', required=True)
    ):
        pass

    @discord.slash_command(
        name='unmute',
        description='un-mutes the specified member',
        guild_ids=[GUILD_ID],
        default_permissions=False
    )
    @permissions.has_any_role(*sum((bot_db.helper_ids | bot_db.mod_ids | bot_db.admin_ids).values(), []))
    async def unmute(
        self,
        ctx,
        offender: Option(discord.Member, name='member', description='Member you wish to un-mute', required=True)
    ):
        pass

    @discord.slash_command(
        name='mute-list',
        description='lists the current muted members',
        guild_ids=[GUILD_ID],
        default_permissions=False
    )
    @permissions.has_any_role(*sum((bot_db.helper_ids | bot_db.mod_ids | bot_db.admin_ids).values(), []))
    async def mute_list(self, ctx):
        pass


def setup(bot):
    bot.add_cog(Mute(bot))
