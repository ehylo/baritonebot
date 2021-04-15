import discord
import logging
from cogs.help import Help
from discord.ext import commands
from cogs.const import helper_group, mod_group, admin_group, muteRole, channel_embed, log_embed, error_embed, logChannel, dm_embed, baritoneDiscord


class Bkm(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.check(admin_group)
    async def unban(self, ctx, user_id: int = None):
        if user_id is None:
            await Help.unban(self, ctx)
        else:
            try:
                user = await self.bot.fetch_user(user_id)
                await ctx.guild.unban(user)
                channel = await self.bot.fetch_channel(logChannel)
                logging.info(f'{ctx.author.id} unbanned {user.id}')
                await channel_embed(ctx, 'User Unbanned', f'{user.name}#{user.discriminator} has been unbanned!')
                await log_embed(ctx, 'User Unbanned', f'{user.name}#{user.discriminator} has been unbanned!', channel)
            except discord.NotFound as e:
                if e.code == 10013:
                    await error_embed(ctx, 'That is not a valid user ID')
                elif e.code == 10026:
                    await error_embed(ctx, 'That user is not banned')

    @commands.command()
    @commands.check(mod_group)
    async def unmute(self, ctx, member: discord.Member = None):
        b_discord = self.bot.get_guild(baritoneDiscord)
        if member is None:
            await Help.unmute(self, ctx)
        elif member.top_role == ctx.author.top_role:
            await error_embed(ctx, f'You don\'t outrank {member.mention}')
        else:
            channel = await self.bot.fetch_channel(logChannel)
            dm_channel = await member.create_dm()
            logging.info(f'{ctx.author.id} unmuted {member.id}')
            await channel_embed(ctx, 'User Unmuted', f'{member.mention} has been unmuted')
            await log_embed(ctx, 'User Unmuted', f'{member.mention} has been unmuted', channel)
            await dm_embed('Unmuted', 'You have been unmuted in the baritone discord', dm_channel)
            await member.remove_roles(b_discord.get_role(muteRole))

    @commands.command()
    @commands.check(mod_group)
    async def ban(self, ctx, member: discord.Member = None, *, reason=None):
        if member is None:
            await Help.ban(self, ctx)
        elif member.top_role == ctx.author.top_role:
            await error_embed(ctx, f'You don\'t outrank {member.mention}')
        elif reason is None:
            await error_embed(ctx, 'You need to give a reason')
        else:
            channel = await self.bot.fetch_channel(logChannel)
            dm_channel = await member.create_dm()
            logging.info(f'{ctx.author.id} banned {member.id} for reason: {reason}')
            await channel_embed(ctx, 'User Banned', f'{member.mention} has been banned for reason: \n```{reason}```')
            await log_embed(ctx, 'User Banned', f'{member.mention} has been banned for reason: \n```{reason}```', channel)
            await dm_embed('Banned', f'You have been banned from the baritone discord for reason: \n```{reason}```', dm_channel)
            await member.ban(reason=reason)

    @commands.command()
    @commands.check(helper_group)
    async def mute(self, ctx, member: discord.Member = None, *, reason=None):
        b_discord = self.bot.get_guild(baritoneDiscord)
        if member is None:
            await Help.mute(self, ctx)
        elif member.top_role == ctx.author.top_role:
            await error_embed(ctx, f'You don\'t outrank {member.mention}')
        elif reason is None:
            await error_embed(ctx, 'You need to give a reason')
        else:
            channel = await self.bot.fetch_channel(logChannel)
            dm_channel = await member.create_dm()
            logging.info(f'{ctx.author.id} muted {member.id} for reason: {reason}')
            await channel_embed(ctx, 'User Muted', f'{member.mention} has been muted for reason: \n```{reason}```')
            await log_embed(ctx, 'User Muted', f'{member.mention} has been muted for reason: \n```{reason}```', channel)
            await dm_embed('Muted', f'You have been muted in the baritone discord for reason: \n```{reason}```', dm_channel)
            await member.add_roles(b_discord.get_role(muteRole))

    @commands.command()
    @commands.check(mod_group)
    async def kick(self, ctx, member: discord.Member = None, *, reason=None):
        if member is None:
            await Help.kick(self, ctx)
        elif member.top_role == ctx.author.top_role:
            await error_embed(ctx, f'You don\'t outrank {member.mention}')
        elif reason is None:
            await error_embed(ctx, 'You need to give a reason')
        else:
            channel = await self.bot.fetch_channel(logChannel)
            dm_channel = await member.create_dm()
            logging.info(f'{ctx.author.id} kicked {member.id} for reason: {reason}')
            await channel_embed(ctx, 'User Kicked', f'{member.mention} has been kicked for reason: \n```{reason}```')
            await log_embed(ctx, 'User Kicked', f'{member.mention} has been kicked for reason: \n```{reason}```', channel)
            await dm_embed('Kicked', f'You have been kicked from the baritone discord for reason: \n```{reason}```', dm_channel)
            await member.kick(reason=reason)


def setup(bot):
    bot.add_cog(Bkm(bot))
