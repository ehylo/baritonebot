import logging

import discord
from discord.ext import commands

from utils import slash_embed, get_channel

log = logging.getLogger('privileged.clear_command')


class Clear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(description='Clear a channel\'s messages or a member\'s messages in a channel')
    @discord.app_commands.default_permissions(ban_members=True)
    @discord.app_commands.describe(
        number='number of messages to clear',
        member='clear messages from this member (if no channel is given then the current channel is chosen)',
        channel='clear messages from this channel (if no member is given it will do messages from all members'
    )
    async def clear(
        self,
        inter: discord.Interaction,
        number: discord.app_commands.Range[int, 1, 1000000],
        member: discord.Member = None,
        channel: discord.TextChannel = None
    ):

        # function to make sure the message being checked matches the chosen member
        def member_check(m):
            return m.author == member

        channel = inter.channel if channel is None else channel
        log_channel = await get_channel(self.bot, self.bot.db.get_logs_channel_id(inter.guild.id))

        # if the person using the command supplied a member then we want to clear only from that person
        if member is not None:
            og_num = number
            limit = 0

            # go through the messages in the history and update the counter based on if it matches or not
            async for message in channel.history(limit=None):
                limit += 1
                if message.author == member:
                    number -= 1
                if number == 0:
                    break

            # once we know how many messages to check, we can purge them
            await channel.purge(limit=limit, check=member_check)
            embed_var = discord.Embed(
                color=self.bot.db.get_embed_color(inter.guild.id),
                description=f'{inter.user.mention} cleared {og_num} messages in {channel.mention} from {member.mention}'
            )
            embed_var.set_footer(
                text=f'{inter.user.name} | ID: {inter.user.id}',
                icon_url=inter.user.display_avatar.url
            )
            await log_channel.send(embed=embed_var)
            await slash_embed(
                inter,
                inter.user,
                f'Successfully cleared {og_num} messages from {member.mention} in {channel.mention}',
                'Bulk messages deleted',
                self.bot.db.get_embed_color(inter.guild.id),
            )
            log.info(f'{inter.user.id} has purged {number} messages from {member.id}')
        else:

            # if no member is provided we can just use built-in functions
            await channel.purge(limit=number)
            embed_var = discord.Embed(
                color=self.bot.db.get_embed_color(inter.guild.id),
                description=f'{inter.user.mention} cleared {number} messages in {channel.mention}'
            )
            embed_var.set_footer(
                text=f'{inter.user.name} | ID: {inter.user.id}',
                icon_url=inter.user.display_avatar.url
            )
            await log_channel.send(embed=embed_var)
            await slash_embed(
                inter,
                inter.user,
                f'Successfully cleared {number} messages in {channel.mention}',
                'Bulk messages deleted',
                self.bot.db.get_embed_color(inter.guild.id),
            )
            log.info(f'{inter.user.id} has purged {number} messages from {channel.id}')


async def setup(bot):
    await bot.add_cog(Clear(bot))
