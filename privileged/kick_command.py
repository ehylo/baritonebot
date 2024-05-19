import logging

import discord
from discord.ext import commands

from utils import role_hierarchy, slash_embed, dm_embed, mod_log_embed

log = logging.getLogger('privileged.kick_command')


class Kick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(description='kicks the specified member')
    @discord.app_commands.default_permissions(ban_members=True)
    @discord.app_commands.describe(offender='Member you wish to kick', reason='The reason you are kicking this member')
    @discord.app_commands.rename(offender='member')
    async def kick(self, inter: discord.Interaction, offender: discord.Member, reason: str):
        if not role_hierarchy(self.bot.db, inter.guild.id, enforcer=inter.user, offender=offender):
            return await slash_embed(inter, inter.user, f'You don\'t outrank {offender.mention}')
        await offender.kick(reason=reason)
        await slash_embed(
            inter,
            inter.user,
            f'{offender.mention} has been kicked for reason: ```{reason}```',
            'Member Kicked',
            self.bot.db.get_embed_color(inter.guild.id),
            ephemeral=False
        )
        await mod_log_embed(
            self.bot,
            self.bot.db,
            inter.guild.id,
            inter.user,
            offender,
            'Member Kicked',
            f'{offender.mention} has been kicked for reason: ```{reason}```'
        )
        dm_channel = await offender.create_dm()
        await dm_embed(
            self.bot.db,
            inter.guild.id,
            channel=dm_channel,
            author=inter.user,
            title='Kicked',
            description=f'You have been kicked from the baritone discord for reason: \n```{reason}```'
        )
        log.info(f'{inter.user.id} has kicked {offender.id} for reason: {reason}')


async def setup(bot):
    await bot.add_cog(Kick(bot))
