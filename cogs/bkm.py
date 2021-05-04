import discord
import logging
import const
from datetime import datetime
from cogs.help import Help
from discord.ext import commands


async def member_check(self, ctx, user):
    member = await self.bot.get_guild(const.baritoneDiscord).fetch_member(user.id)
    author_member = await self.bot.get_guild(const.baritoneDiscord).fetch_member(ctx.author.id)
    return member, author_member


class Bkm(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['ub'])
    @commands.check(const.mod_group)
    async def unban(self, ctx, user=None):
        try:
            user_men = str(ctx.message.raw_mentions[0])
        except IndexError:
            user_men = ''
        b_guild = self.bot.get_guild(const.baritoneDiscord)
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
                await const.error_embed(ctx, 'The user you gave is invalid')
            else:
                try:
                    user = await self.bot.fetch_user(user)
                    await b_guild.unban(unban_user)
                    channel = await self.bot.fetch_channel(const.modlogChannel)
                    logging.info(f'{ctx.author.id} unbanned {user.id}')
                    await const.channel_embed(ctx, 'User Unbanned', f'{user.name}#{user.discriminator} has been unbanned!')
                    await const.log_embed(ctx, 'User Unbanned', f'{user.name}#{user.discriminator} has been unbanned!', channel)
                except discord.NotFound:
                    await const.error_embed(ctx, 'That user is not banned')

    @commands.command(aliases=['um'])
    @commands.check(const.mod_group)
    async def unmute(self, ctx, user: discord.User = None):
        member, author_member = await member_check(self, ctx, user)
        if member is None:
            await Help.unmute(self, ctx)
        elif member.top_role == author_member.top_role:
            await const.error_embed(ctx, f'You don\'t outrank {member.mention}')
        else:
            if self.bot.get_guild(const.baritoneDiscord).get_role(const.muteRole) not in member.roles:
                await const.error_embed(ctx, 'That member is not muted')
            else:
                await member.remove_roles(self.bot.get_guild(const.baritoneDiscord).get_role(const.muteRole))
                try:
                    dm_channel = await member.create_dm()
                    await const.dm_embed('Unmuted', 'You have been unmuted in the baritone discord', dm_channel)
                except (discord.Forbidden, discord.errors.HTTPException):
                    pass
                channel = await self.bot.fetch_channel(const.modlogChannel)
                logging.info(f'{ctx.author.id} unmuted {member.id}')
                await const.channel_embed(ctx, 'User Unmuted', f'{member.mention} has been unmuted')
                await const.log_embed(ctx, 'User Unmuted', f'{member.mention} has been unmuted', channel)
                const.cur.execute('DELETE FROM punish WHERE user_id=%s', (user.id,))
                const.db.commit()

    @commands.command(aliases=['b', 'rm'])
    @commands.check(const.mod_group)
    async def ban(self, ctx, user: discord.User = None, purge=None, *, reason=None):
        member, author_member = await member_check(self, ctx, user)
        if member is None:
            await Help.ban(self, ctx)
        elif member.top_role == author_member.top_role:
            await const.error_embed(ctx, f'You don\'t outrank {member.mention}')
        elif purge is None:
            await const.error_embed(ctx, 'You need to give a reason')
        else:
            async def ban_embeds(reasons):
                try:
                    dm_channel = await member.create_dm()
                    await const.dm_embed('Banned', f'You have been banned from the baritone discord for reason: \n```{reasons}```', dm_channel)
                except (discord.Forbidden, discord.errors.HTTPException):
                    pass
                channel = await self.bot.fetch_channel(const.modlogChannel)
                logging.info(f'{ctx.author.id} banned {member.id} for reason: {reasons}')
                await const.channel_embed(ctx, 'User Banned', f'{member.mention} has been banned for reason: \n```{reasons}```')
                await const.log_embed(ctx, 'User Banned', f'{member.mention} has been banned for reason: \n```{reasons}```', channel)
            if purge.lower() == 'purge':
                await ban_embeds(reason)
                await member.ban(reason=reason, delete_message_days=7)
            else:
                await ban_embeds(f'{purge} {reason}')
                await member.ban(reason=reason, delete_message_days=0)

    @commands.command(aliases=['m'])
    @commands.check(const.helper_group)
    async def mute(self, ctx, user: discord.User = None, time=None, *, reason=None):
        member, author_member = await member_check(self, ctx, user)
        if member is None:
            await Help.mute(self, ctx)
        elif member.top_role == author_member.top_role:
            await const.error_embed(ctx, f'You don\'t outrank {member.mention}')
        elif time is None:
            await const.error_embed(ctx, 'You need to give a reason or amount of time to mute')
        elif (time[0].isdigit()) and (reason is None):
            await const.error_embed(ctx, 'You need to give a reason')
        else:
            if self.bot.get_guild(const.baritoneDiscord).get_role(const.muteRole) in member.roles:
                await const.error_embed(ctx, 'That member is already muted')
            else:
                async def mute_embeds(time_muted, usert, amountt, multiplyt, year, month, day, hour, minute):
                    await member.add_roles(self.bot.get_guild(const.baritoneDiscord).get_role(const.muteRole))
                    try:
                        dm_channel = await member.create_dm()
                        await const.dm_embed('Muted', f'You have been muted in the baritone discord {time_muted}, reason: \n```{reason}```', dm_channel)
                    except (discord.Forbidden, discord.errors.HTTPException):
                        pass
                    channel = await self.bot.fetch_channel(const.modlogChannel)
                    logging.info(f'{ctx.author.id} muted {member.id} {time_muted}, reason: {reason}')
                    await const.channel_embed(ctx, 'User Muted', f'{member.mention} has been muted {time_muted}, reason: \n```{reason}```')
                    await const.log_embed(ctx, 'User Muted', f'{member.mention} has been muted {time_muted}, reason: \n```{reason}```', channel)
                    const.cur.execute(
                        "INSERT INTO punish(user_id, amount_time, what_time, against, year, month, day, hour, minute) "
                        "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                        (usert, amountt, multiplyt, 'muted', year, month, day, hour, minute))
                    const.db.commit()
                x = datetime.utcnow()
                if time[0].isdigit():
                    multiply = ''.join(i for i in time if not i.isdigit())
                    amount = ''.join(i for i in time if i.isdigit())
                    if len(multiply) > 1:
                        await const.error_embed(ctx, 'Only use \'m\'(minutes), \'h\'(hours), or \'d\'(days).')
                    else:
                        await mute_embeds(f'for {time}', user.id, amount, multiply, x.year, x.month, x.day, x.hour, x.minute)
                else:
                    await mute_embeds('indefinitely', user.id, '0', 'f', x.year, x.month, x.day, x.hour, x.minute)

    @commands.command(aliases=['k'])
    @commands.check(const.mod_group)
    async def kick(self, ctx, user: discord.User = None, *, reason=None):
        member, author_member = await member_check(self, ctx, user)
        if member is None:
            await Help.kick(self, ctx)
        elif member.top_role == author_member.top_role:
            await const.error_embed(ctx, f'You don\'t outrank {member.mention}')
        elif reason is None:
            await const.error_embed(ctx, 'You need to give a reason')
        else:
            try:
                dm_channel = await member.create_dm()
                await const.dm_embed('Kicked', f'You have been kicked from the baritone discord for reason: \n```{reason}```', dm_channel)
            except (discord.Forbidden, discord.errors.HTTPException):
                pass
            channel = await self.bot.fetch_channel(const.modlogChannel)
            logging.info(f'{ctx.author.id} kicked {member.id} for reason: {reason}')
            await const.channel_embed(ctx, 'User Kicked', f'{member.mention} has been kicked for reason: \n```{reason}```')
            await const.log_embed(ctx, 'User Kicked', f'{member.mention} has been kicked for reason: \n```{reason}```', channel)
            await member.kick(reason=reason)


def setup(bot):
    bot.add_cog(Bkm(bot))
