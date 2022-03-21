import discord
from discord.ext import commands
from discord.commands import permissions, Option

from main import bot_db
from utils import embeds
from utils.const import GUILD_ID
from utils.misc import role_hierarchy, get_user


class Ban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(
        name='ban',
        description='bans the specified member',
        guild_ids=[GUILD_ID],
        default_permissions=False
    )
    @permissions.has_any_role(*sum((bot_db.mod_ids | bot_db.admin_ids).values(), []))
    async def ban(
        self,
        ctx,
        offender: Option(discord.Member, name='member', description='Member you wish to ban', required=True),
        purge: Option(
            int,
            name='days',
            description='# of days you want to purge messages from this member',
            choices=[0, 1, 2, 3, 4, 5, 6, 7],
            required=True,
            default=0
        ),
        reason: Option(str, name='reason', description='The reason you are banning this member', required=True)
    ):
        if not role_hierarchy(bot_db, ctx.guild.id, enforcer=ctx.author, offender=offender):
            return await embeds.slash_embed(ctx, ctx.author, f'You don\'t outrank {offender.mention}')
        await embeds.slash_embed(
            ctx,
            ctx.author,
            f'{offender.mention} has been banned for reason: ```{reason}```',
            'Member Banned',
            bot_db.embed_color[ctx.guild.id],
            ephemeral=False
        )
        await embeds.mod_log_embed(
            self.bot,
            bot_db,
            ctx.guild.id,
            ctx.author,
            offender,
            'Member Banned',
            f'{offender.mention} has been banned for reason: ```{reason}```'
        )
        dm_channel = await offender.create_dm()
        await embeds.dm_embed(
            bot_db,
            ctx.guild.id,
            channel=dm_channel,
            author=ctx.author,
            title='Banned',
            description=f'You have been banned in the baritone discord for reason: \n```{reason}```'
        )
        await offender.ban(reason=reason, delete_message_days=purge)

    @discord.slash_command(
        name='unban',
        description='unbans the specified user',
        guild_ids=[GUILD_ID],
        default_permissions=False
    )
    @permissions.has_any_role(*sum((bot_db.mod_ids | bot_db.admin_ids).values(), []))
    async def unban(
        self,
        ctx,
        user_id: Option(discord.User, name='user', description='User you want to unban', required=True)
    ):
        try:
            user = await get_user(self.bot, user_id)
            await ctx.guild.unban(user)
            await embeds.slash_embed(
                ctx,
                ctx.author,
                f'{user.mention} has been unbanned',
                'User Unbanned',
                bot_db.embed_color[ctx.guild.id],
                ephemeral=False
            )
        except discord.NotFound:
            return await embeds.slash_embed(ctx, ctx.author, 'That user is not banned', 'Not Found')


def setup(bot):
    bot.add_cog(Ban(bot))
