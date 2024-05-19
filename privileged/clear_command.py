import discord
from discord.ext import commands

from utils import slash_embed, get_channel


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

        def member_check(m):
            return m.author == member

        channel = inter.channel if channel is None else channel
        log_channel = await get_channel(self.bot, self.bot.db.get_logs_channel_id(inter.guild.id))
        if member is not None:
            og_num = number
            limit = 0
            async for message in channel.history(limit=None):
                limit += 1
                if message.author == member:
                    number -= 1
                if number == 0:
                    break
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
        else:
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


async def setup(bot):
    await bot.add_cog(Clear(bot))
