import logging
from typing import Literal

import discord
from discord.ext import commands

from utils import slash_embed, role_hierarchy, mod_log_embed, dm_embed

log = logging.getLogger('privileged.ban_command')


class Ban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.default_permissions(ban_members=True)
    @discord.app_commands.command(name='ban', description='bans the specified member')
    @discord.app_commands.rename(offender='member', purge='days')
    @discord.app_commands.describe(
        offender='Member you wish to ban',
        purge='# of days you want to purge messages from this member',
        reason='The reason you are banning this member'
    )
    async def ban(
        self, inter: discord.Interaction, offender: discord.Member, purge: Literal[0, 1, 2, 3, 4, 5, 6, 7], reason: str
    ):

        # make sure the person they are trying to ban isn't above them
        if not role_hierarchy(self.bot.db, inter.guild.id, enforcer=inter.user, offender=offender):
            return await slash_embed(inter, inter.user, f'You don\'t outrank {offender.mention}')

        # ban and send the appropriate embeds
        await offender.ban(reason=reason, delete_message_days=purge)
        await slash_embed(
            inter,
            inter.user,
            f'{offender.mention} has been banned for reason: ```{reason}```',
            'Member Banned',
            self.bot.db.get_embed_color(inter.guild.id),
            ephemeral=False
        )
        await mod_log_embed(
            self.bot,
            self.bot.db,
            inter.guild.id,
            inter.user,
            offender,
            'Member Banned',
            f'{offender.mention} has been banned for reason: ```{reason}```'
        )
        dm_channel = await offender.create_dm()
        await dm_embed(
            self.bot.db,
            inter.guild.id,
            channel=dm_channel,
            author=inter.user,
            title='Banned',
            description=f'You have been banned in the baritone discord for reason: \n```{reason}```'
        )
        log.info(f'{inter.user.id} has banned {offender.id}, purging {purge} with reason: {reason}')

    @discord.app_commands.default_permissions(ban_members=True)
    @discord.app_commands.command(name='unban', description='unbans the specified user')
    @discord.app_commands.describe(user='User you want to unban')
    async def unban(self, inter: discord.Interaction, user: discord.User):
        try:
            await inter.guild.unban(user)
            await slash_embed(
                inter,
                inter.user,
                f'{user.mention} has been unbanned',
                'User Unbanned',
                self.bot.db.get_embed_color(inter.guild.id),
                ephemeral=False
            )
            log.info(f'{inter.user.id} has unbanned {user.id}')
        except discord.NotFound:  # make sure they are actually banned
            return await slash_embed(inter, inter.user, 'That user is not banned', 'Not Found')


async def setup(bot):
    await bot.add_cog(Ban(bot))
