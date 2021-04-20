import discord
import logging
from cogs.help import Help
from discord.ext import commands
from const import helper_group, mod_group, admin_group, muteRole, channel_embed, log_embed, error_embed, logChannel, dm_embed, baritoneDiscord


class Bkm(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['ub'])
    @commands.check(admin_group)
    async def unban(self, ctx, user=None):
        user_men = str(ctx.message.raw_mentions[0])[1:-1]
        b_guild = self.bot.get_guild(baritoneDiscord)
        if user is None:
            await Help.unban(self, ctx)
        else:
            if user_men != '':
                unban_user = self.bot.get_user(int(user_men))  # get the user if they mentioned
            elif (user.isdigit()) and (len(user) == 18):
                unban_user = self.bot.get_user(int(user))
            else:
                unban_user = None
            if unban_user is None:
                await error_embed(ctx, 'The user you gave is invalid')
            else:
                try:
                    user = await self.bot.fetch_user(user)
                    await b_guild.unban(unban_user)
                    channel = await self.bot.fetch_channel(logChannel)
                    logging.info(f'{ctx.author.id} unbanned {user.id}')
                    await channel_embed(ctx, 'User Unbanned', f'{user.name}#{user.discriminator} has been unbanned!')
                    await log_embed(ctx, 'User Unbanned', f'{user.name}#{user.discriminator} has been unbanned!', channel)
                except discord.NotFound:
                    await error_embed(ctx, 'That user is not banned')

    @commands.command(aliases=['um'])
    @commands.check(mod_group)
    async def unmute(self, ctx, user: discord.User = None):
        b_guild = self.bot.get_guild(baritoneDiscord)
        member = await b_guild.fetch_member(user.id)
        author_member = await b_guild.fetch_member(ctx.author.id)
        if member is None:
            await Help.unmute(self, ctx)
        elif member.top_role == author_member.top_role:
            await error_embed(ctx, f'You don\'t outrank {member.mention}')
        else:
            if b_guild.get_role(muteRole) not in member.roles:
                await error_embed(ctx, 'That member is not muted')
            else:
                channel = await self.bot.fetch_channel(logChannel)
                dm_channel = await member.create_dm()
                logging.info(f'{ctx.author.id} unmuted {member.id}')
                await channel_embed(ctx, 'User Unmuted', f'{member.mention} has been unmuted')
                await log_embed(ctx, 'User Unmuted', f'{member.mention} has been unmuted', channel)
                await dm_embed('Unmuted', 'You have been unmuted in the baritone discord', dm_channel)
                await member.remove_roles(b_guild.get_role(muteRole))

    @commands.command(aliases=['b', 'rm'])
    @commands.check(mod_group)
    async def ban(self, ctx, user: discord.User = None, *, reason=None):
        b_guild = self.bot.get_guild(baritoneDiscord)
        member = await b_guild.fetch_member(user.id)
        author_member = await b_guild.fetch_member(ctx.author.id)
        if member is None:
            await Help.ban(self, ctx)
        elif member.top_role == author_member.top_role:
            await error_embed(ctx, f'You don\'t outrank {member.mention}')
        elif reason is None:
            await error_embed(ctx, 'You need to give a reason')
        else:
            if b_guild.get_role(muteRole) in member.roles:
                await error_embed(ctx, 'That member is already muted')
            else:
                channel = await self.bot.fetch_channel(logChannel)
                dm_channel = await member.create_dm()
                logging.info(f'{ctx.author.id} banned {member.id} for reason: {reason}')
                await channel_embed(ctx, 'User Banned', f'{member.mention} has been banned for reason: \n```{reason}```')
                await log_embed(ctx, 'User Banned', f'{member.mention} has been banned for reason: \n```{reason}```', channel)
                await dm_embed('Banned', f'You have been banned from the baritone discord for reason: \n```{reason}```', dm_channel)
                await member.ban(reason=reason)

    @commands.command(aliases=['m'])
    @commands.check(helper_group)
    async def mute(self, ctx, user: discord.User = None, *, reason=None):
        b_guild = self.bot.get_guild(baritoneDiscord)
        member = await b_guild.fetch_member(user.id)
        author_member = await b_guild.fetch_member(ctx.author.id)
        if member is None:
            await Help.mute(self, ctx)
        elif member.top_role == author_member.top_role:
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
            await member.add_roles(b_guild.get_role(muteRole))

    @commands.command(aliases=['k'])
    @commands.check(mod_group)
    async def kick(self, ctx, user: discord.User = None, *, reason=None):
        b_guild = self.bot.get_guild(baritoneDiscord)
        member = await b_guild.fetch_member(user.id)
        author_member = await b_guild.fetch_member(ctx.author.id)
        if member is None:
            await Help.kick(self, ctx)
        elif member.top_role == author_member.top_role:
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
