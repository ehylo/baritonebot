from typing import Literal

import discord
from discord.ext import commands

from utils import embeds
from utils.misc import role_hierarchy


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
        if not role_hierarchy(self.bot.db, inter.guild.id, enforcer=inter.user, offender=offender):
            return await embeds.slash_embed(inter, inter.user, f'You don\'t outrank {offender.mention}')
        await offender.ban(reason=reason, delete_message_days=purge)
        await embeds.slash_embed(
            inter,
            inter.user,
            f'{offender.mention} has been banned for reason: ```{reason}```',
            'Member Banned',
            self.bot.db.embed_color[inter.guild.id],
            ephemeral=False
        )
        await embeds.mod_log_embed(
            self.bot,
            self.bot.db,
            inter.guild.id,
            inter.user,
            offender,
            'Member Banned',
            f'{offender.mention} has been banned for reason: ```{reason}```'
        )
        dm_channel = await offender.create_dm()
        await embeds.dm_embed(
            self.bot.db,
            inter.guild.id,
            channel=dm_channel,
            author=inter.user,
            title='Banned',
            description=f'You have been banned in the baritone discord for reason: \n```{reason}```'
        )

    @discord.app_commands.default_permissions(ban_members=True)
    @discord.app_commands.command(name='unban', description='unbans the specified user')
    @discord.app_commands.describe(user='User you want to unban')
    async def unban(self, inter: discord.Interaction, user: discord.User):
        try:
            await inter.guild.unban(user)
            await embeds.slash_embed(
                inter,
                inter.user,
                f'{user.mention} has been unbanned',
                'User Unbanned',
                self.bot.db.embed_color[inter.guild.id],
                ephemeral=False
            )
        except discord.NotFound:
            return await embeds.slash_embed(inter, inter.user, 'That user is not banned', 'Not Found')


async def setup(bot):
    await bot.add_cog(Ban(bot))
