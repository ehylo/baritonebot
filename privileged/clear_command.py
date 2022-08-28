import discord
from discord.ext import commands
from discord.commands import Option

from utils.const import GUILD_ID
from utils.embeds import slash_embed
from utils.misc import get_channel
from main import bot_db


class Clear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(
        name='clear',
        description='Clear a channel\'s messages or a member\'s messages in a channel',
        guild_ids=[GUILD_ID]
    )
    @discord.default_permissions(ban_members=True)
    async def clear(
        self,
        ctx,
        num: Option(
            int,
            name='number',
            description='number of messages to clear',
            min_value=1,
            max_value=1000000,
            required=True
        ),
        member: Option(
            discord.Member,
            name='member',
            description='clear messages from this member (if no channel is given then the current channel is chosen)'
        ) = None,
        channel: Option(
            discord.TextChannel,
            name='channel',
            description='clear messages from this channel (if no member is given it will do messages from all members'
        ) = None
    ):

        def member_check(m):
            return m.author == member

        channel = ctx.channel if channel is None else channel
        log_channel = await get_channel(self.bot, bot_db.logs_id[ctx.guild.id])
        if member is not None:
            og_num = num
            limit = 0
            async for message in channel.history(limit=None):
                limit += 1
                if message.author == member:
                    num -= 1
                if num == 0:
                    break
            await channel.purge(limit=limit, check=member_check, bulk=True)
            embed_var = discord.Embed(
                color=bot_db.embed_color[ctx.guild.id],
                description=f'{ctx.author.mention} cleared {og_num} messages in {channel.mention} from {member.mention}'
            )
            embed_var.set_footer(
                text=f'{ctx.author.name} | ID: {ctx.author.id}',
                icon_url=ctx.author.display_avatar.url
            )
            await log_channel.send(embed=embed_var)
            await slash_embed(
                ctx,
                ctx.author,
                f'Successfully cleared {og_num} messages from {member.mention} in {channel.mention}',
                'Bulk messages deleted',
                bot_db.embed_color[ctx.guild.id],
            )
        else:
            await channel.purge(limit=num, bulk=True)
            embed_var = discord.Embed(
                color=bot_db.embed_color[ctx.guild.id],
                description=f'{ctx.author.mention} cleared {num} messages in {channel.mention}'
            )
            embed_var.set_footer(
                text=f'{ctx.author.name} | ID: {ctx.author.id}',
                icon_url=ctx.author.display_avatar.url
            )
            await log_channel.send(embed=embed_var)
            await slash_embed(
                ctx,
                ctx.author,
                f'Successfully cleared {num} messages in {channel.mention}',
                'Bulk messages deleted',
                bot_db.embed_color[ctx.guild.id],
            )


def setup(bot):
    bot.add_cog(Clear(bot))
