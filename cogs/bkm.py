import discord
import main
import re
from time import time
from cogs.help import Help
from discord.ext import commands


def role_hierarchy(punisher, against):
    punisher_roles = []
    against_roles = []
    for role in punisher.roles:
        punisher_roles.append(role.id)
    for role in against.roles:
        against_roles.append(role.id)
    if any(i in [main.ids(8), main.ids(10), main.ids(7)] for i in against_roles) is True:  # checks if the against person has dev/admin/bypassed
        return False
    if main.ids(9) in against_roles:  # checks if the against person has mod
        if any(i in [main.ids(8), main.ids(10), main.ids(7)] for i in punisher_roles) is True:
            return True
    elif main.ids(6) in against_roles:  # checks if the against person has helper
        if any(i in [main.ids(8), main.ids(10), main.ids(7), main.ids(9)] for i in punisher_roles) is True:
            return True
    else:
        return True if any(i in [main.ids(8), main.ids(10), main.ids(7), main.ids(9), main.ids(6)] for i in punisher_roles) is True else False


time_regex = re.compile(r'^(\d+)([a-z])$')
time_dict = {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800, "y": 31536000}


class TimeConverter(commands.Converter):
    async def convert(self, ctx, argument):
        args = argument.lower()
        mute_time = 0
        for digit, amount in re.findall(time_regex, args):
            mute_time = 0
            try:
                mute_time += int((time_dict[amount] * float(digit)) + int(time()))
                if mute_time >= (9223372036854775800 - int(time())):
                    return mute_time, args, False, 2
            except KeyError:
                return mute_time, args, False, 1
            except ValueError:
                pass
        return mute_time, args, True, 0


class Bkm(commands.Cog):
    def __init__(self, bot):
        """Returns embeds for all the punishment commands."""
        self.bot = bot

    @commands.command(aliases=['ub'])
    @commands.check(main.mod_group)
    async def unban(self, ctx, user: discord.User = None):
        if user is None:
            return await Help.unban(self, ctx)
        try:
            await self.bot.get_guild(main.ids(1)).unban(user)
            await main.channel_embed(ctx, 'User Unbanned', f'{user.mention} has been unbanned')
            print(f'{ctx.author.id} unbanned {user.id}')
            channel = await self.bot.fetch_channel(main.ids(5))
            await main.log_embed(ctx, 'User Unbanned', f'{user.mention} has been unbanned', channel, user)
        except discord.NotFound:
            await main.error_embed(ctx, 'That user is not banned')

    @commands.command(aliases=['um'])
    @commands.check(main.mod_group)
    async def unmute(self, ctx, user: discord.User = None):
        if user is None:
            return await Help.unmute(self, ctx)
        try:
            saver = await self.bot.get_guild(main.ids(1)).fetch_member(ctx.author.id)
            unmuted_user = await self.bot.get_guild(main.ids(1)).fetch_member(user.id)
            if role_hierarchy(saver, unmuted_user) is not True:
                return await main.error_embed(ctx, f'You don\'t outrank {unmuted_user.mention}')
            if self.bot.get_guild(main.ids(1)).get_role(main.ids(12)) not in unmuted_user.roles:
                return await main.error_embed(ctx, 'That member is not muted')
            await unmuted_user.remove_roles(self.bot.get_guild(main.ids(1)).get_role(main.ids(12)))
            await main.channel_embed(ctx, 'User Unmuted', f'{unmuted_user.mention} has been unmuted')
            try:
                dm_channel = await unmuted_user.create_dm()
                await main.dm_embed('Unmuted', 'You have been unmuted in the baritone discord', dm_channel)
            except (discord.Forbidden, discord.errors.HTTPException):
                pass
            print(f'{ctx.author.id} unmuted {unmuted_user.id}')
            channel = await self.bot.fetch_channel(main.ids(5))
            await main.log_embed(ctx, 'User Unmuted', f'{unmuted_user.mention} has been unmuted', channel, unmuted_user)
            main.cur.execute('DELETE FROM rekt WHERE user_id=%s', (user.id,))
            main.db.commit()
        except discord.NotFound:
            await main.error_embed(ctx, 'That is not a valid member')

    @commands.command(aliases=['b', 'rm'])
    @commands.check(main.mod_group)
    async def ban(self, ctx, user: discord.User = None, do_purge=None, *, reason=None):
        if user is None:
            return await Help.ban(self, ctx)
        if (do_purge is None) or ((do_purge.lower() == 'purge') and (reason is None)):
            return await main.error_embed(ctx, 'You need to give a reason')
        try:
            punisher = await self.bot.get_guild(main.ids(1)).fetch_member(ctx.author.id)
            banned_user = await self.bot.get_guild(main.ids(1)).fetch_member(user.id)
            if role_hierarchy(punisher, banned_user) is not True:
                return await main.error_embed(ctx, f'You don\'t outrank {banned_user.mention}')
            reason = '' if reason is None else reason
            ban_reason = reason if do_purge.lower() == 'purge' else f'{do_purge} {reason}'
            await main.channel_embed(ctx, 'Member Banned', f'{banned_user.mention} has been banned for reason: ```{ban_reason}```')
            try:
                dm_channel = await banned_user.create_dm()
                await main.dm_embed('Banned', f'You have been banned in the baritone discord for reason: \n```{ban_reason}```', dm_channel)
            except (discord.Forbidden, discord.errors.HTTPException):
                pass
            print(f'{ctx.author.id} banned {banned_user.id} for reason: {ban_reason}')
            channel = await self.bot.fetch_channel(main.ids(5))
            await main.log_embed(ctx, 'Member Banned', f'{banned_user.mention} has been banned for reason: ```{ban_reason}```', channel, banned_user)
            purge_days = 7 if do_purge.lower() == 'purge' else 0
            await banned_user.ban(reason=ban_reason, delete_message_days=purge_days)
        except discord.NotFound:
            await main.error_embed(ctx, 'That is not a valid member')

    @commands.group(invoke_without_command=True, case_insensitive=True, aliases=['m'])
    @commands.check(main.helper_group)
    async def mute(self, ctx, user: discord.User = None, mute_time: TimeConverter = None, *, reason=None):
        if user is None:
            return await Help.mute(self, ctx)
        if mute_time is None:
            return await main.error_embed(ctx, 'You need to give a reason or time')
        try:
            punisher = await self.bot.get_guild(main.ids(1)).fetch_member(ctx.author.id)
            muted_user = await self.bot.get_guild(main.ids(1)).fetch_member(user.id)
            if role_hierarchy(punisher, muted_user) is not True:  # check if they have the correct roles
                return await main.error_embed(ctx, f'You don\'t outrank {muted_user.mention}')
            if self.bot.get_guild(main.ids(1)).get_role(main.ids(12)) in muted_user.roles:  # check if they are already muted
                return await main.error_embed(ctx, 'That member is already muted')
            if mute_time[3] == 1:  # check if an incorrect time was given
                return await main.error_embed(ctx, 'Only use `s`(seconds), `m`(minutes), `h`(hours), `d`(days), `w`(weeks), or `y`(years).')
            if mute_time[3] == 2:  # check if someone is trying to break the bot
                return await main.error_embed(ctx, 'That time in seconds is larger than 64 bits which isn\'t supported by postgreSQL, please chose a shorter time')
            if mute_time[2] is True:  # check if a correct mute time argument was given
                if (reason is None) and (mute_time[0] != 0):  # make sure they provide a reason if they gave a time
                    return await main.error_embed(ctx, 'You need to give a reason')
                await muted_user.add_roles(self.bot.get_guild(main.ids(1)).get_role(main.ids(12)))  # add the mute role
                if mute_time[0] == 0:  # check if they gave a time or not
                    reason = '' if reason is None else reason
                    mute_reason = f'{mute_time[1]} {reason}'
                    amount = 'indefinitely'
                else:
                    mute_reason = reason
                    amount = f'for {mute_time[1]}'
                await main.channel_embed(ctx, 'Member Muted', f'{muted_user.mention} has been muted {amount} for reason: ```{mute_reason}```')
                try:
                    dm_channel = await muted_user.create_dm()
                    await main.dm_embed('Muted', f'You have been muted in the baritone discord {amount} for reason: \n```{mute_reason}```', dm_channel)
                except (discord.Forbidden, discord.errors.HTTPException):
                    pass
                print(f'{ctx.author.id} muted {muted_user.id} {amount} for reason: {mute_reason}')
                channel = await self.bot.fetch_channel(main.ids(5))
                await main.log_embed(ctx, 'Member Muted', f'{muted_user.mention} has been muted {amount} for reason: ```{mute_reason}```', channel, muted_user)
                main.cur.execute('INSERT INTO rekt(user_id, action, expiry, punisher) VALUES(%s, %s, %s, %s)', (muted_user.id, 'muted', int(mute_time[0]), ctx.author.id))
                main.db.commit()
        except discord.NotFound:
            await main.error_embed(ctx, 'That is not a valid member')

    @mute.command(aliases=['l'])
    @commands.check(main.helper_group)
    async def list(self, ctx):
        main.cur.execute("SELECT user_id, expiry FROM rekt WHERE action='muted'")
        muted_users = main.cur.fetchall()
        desc = ''
        for muted_user in muted_users:
            user = await self.bot.fetch_user(muted_user[0])
            remaining = 'indefinite' if muted_user[1] == 0 else main.time_convert(muted_user[1] - int(time()))
            desc += f'**{user} ({user.id}) Time remaining:** \n{remaining}\n'
        await main.channel_embed(ctx, f'Muted Users ({len(muted_users)}):', desc)

    @commands.command(aliases=['k'])
    @commands.check(main.mod_group)
    async def kick(self, ctx, user: discord.User = None, *, reason=None):
        if user is None:
            return await Help.kick(self, ctx)
        if reason is None:
            return await main.error_embed(ctx, 'You need to give a reason')
        try:
            punisher = await self.bot.get_guild(main.ids(1)).fetch_member(ctx.author.id)
            kicked_user = await self.bot.get_guild(main.ids(1)).fetch_member(user.id)
            if role_hierarchy(punisher, kicked_user) is not True:
                return await main.error_embed(ctx, f'You don\'t outrank {kicked_user.mention}')
            await main.channel_embed(ctx, 'Member Kicked', f'{kicked_user.mention} has been kicked for reason: ```{reason}```')
            try:
                dm_channel = await kicked_user.create_dm()
                await main.dm_embed('Kicked', f'You have been kicked in the baritone discord for reason: \n```{reason}```', dm_channel)
            except (discord.Forbidden, discord.errors.HTTPException):
                pass
            print(f'{ctx.author.id} kicked {kicked_user.id} for reason: {reason}')
            channel = await self.bot.fetch_channel(main.ids(5))
            await main.log_embed(ctx, 'Member Kicked', f'{kicked_user.mention} has been kicked for reason: ```{reason}```', channel, kicked_user)
            await kicked_user.kick(reason=reason)
        except discord.NotFound:
            await main.error_embed(ctx, 'That is not a valid member')

    @commands.command()
    async def optout(self, ctx, *, arg=None):
        if arg is None:
            return await Help.optout(self, ctx)
        if arg == 'I am sure':
            opter = self.bot.get_guild(main.ids(1)).get_member(ctx.author.id)
            await main.channel_embed(ctx, 'Member Opted out', f'{opter.mention} has been banned for reason: \n```User {opter} has opted out```')
            try:
                dm_channel = await opter.create_dm()
                await main.dm_embed(
                    'Opted out',
                    'You have been banned for opting out, this is not reverisable and DMing mods asking to be unbanned will just get you blocked',
                    dm_channel
                )
            except (discord.Forbidden, discord.errors.HTTPException):
                pass
            print(f'{opter.id} has been banned for reason: Opted out')
            channel = await self.bot.fetch_channel(main.ids(5))
            await main.log_embed(ctx, 'Member Opted out', f'{opter.mention} has been banned', channel, opter)
            await self.bot.get_guild(main.ids(1)).ban(user=opter, reason='Opted out and banned', delete_message_days=7)
        else:
            await main.channel_embed(
                ctx,
                'Opt out',
                f'You will be **banned from this server** and **lose all your roles** by continuing. Are you sure you want to opt out? if yes, type `{main.values(0)}optout I am sure` (this does work in DMs!)'
            )


def setup(bot):
    bot.add_cog(Bkm(bot))
