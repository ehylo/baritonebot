import discord
from discord.commands import Option
from discord.ext import commands

from utils.const import GUILD_ID
from utils.misc import role_hierarchy
from utils import embeds
from main import bot_db


class Kick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(
        name='kick',
        description='kicks the specified member',
        guild_ids=[GUILD_ID]
    )
    @discord.default_permissions(ban_members=True)
    async def kick(
        self,
        ctx,
        offender: Option(discord.Member, name='member', description='Member you wish to kick', required=True),
        reason: Option(ame='reason', description='The reason you are kicking this member', required=True)
    ):
        if not role_hierarchy(bot_db, ctx.guild.id, enforcer=ctx.author, offender=offender):
            return await embeds.slash_embed(ctx, ctx.author, f'You don\'t outrank {offender.mention}')
        await embeds.slash_embed(
            ctx,
            ctx.author,
            f'{offender.mention} has been kicked for reason: ```{reason}```',
            'Member Kicked',
            bot_db.embed_color[ctx.guild.id],
            ephemeral=False
        )
        await embeds.mod_log_embed(
            self.bot,
            bot_db,
            ctx.guild.id,
            ctx.author,
            offender,
            'Member Kicked',
            f'{offender.mention} has been kicked for reason: ```{reason}```'
        )
        dm_channel = await offender.create_dm()
        await embeds.dm_embed(
            bot_db,
            ctx.guild.id,
            channel=dm_channel,
            author=ctx.author,
            title='Kicked',
            description=f'You have been kicked from the baritone discord for reason: \n```{reason}```'
        )
        await offender.kick(reason=reason)


def setup(bot):
    bot.add_cog(Kick(bot))
