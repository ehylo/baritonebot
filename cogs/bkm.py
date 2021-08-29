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
    if any(i in [main.ids(8), main.ids(9), main.ids(11)] for i in against_roles) is True:  # checks if the against person has dev/admin/bypassed
        return False
    if main.ids(10) in against_roles:  # checks if the against person has mod
        if any(i in [main.ids(8), main.ids(9), main.ids(11)] for i in punisher_roles) is True:
            return True
    elif main.ids(7) in against_roles:  # checks if the against person has helper
        if any(i in [main.ids(8), main.ids(9), main.ids(11), main.ids(10)] for i in punisher_roles) is True:
            return True
    else:
        return True if any(i in [main.ids(8), main.ids(9), main.ids(11), main.ids(10), main.ids(7)] for i in punisher_roles) is True else False


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
        return mute_time, args, True


class Bkm(commands.Cog):
    def __init__(self, bot):
        """Returns embeds for all the punishment commands."""
        self.bot = bot

    @commands.command(aliases=['ub'])
    @commands.check(main.mod_group)
    async def unban(self, ctx):
        pass

    @commands.command(aliases=['um'])
    @commands.check(main.mod_group)
    async def unmute(self, ctx):
        pass

    @commands.command(aliases=['b', 'rm'])
    @commands.check(main.mod_group)
    async def ban(self, ctx):
        pass

    @commands.group(invoke_without_command=True, case_insensitive=True, aliases=['m'])
    @commands.check(main.helper_group)
    async def mute(self, ctx, user: discord.User = None, mute_time: TimeConverter = None, *, reason=None):
        if user is None:
            await Help.mute(self, ctx)
        elif mute_time is None:
            await main.error_embed(ctx, 'You need to give a reason or time')
        else:
            try:
                punisher = await self.bot.get_guild(main.ids(1)).fetch_member(ctx.author.id)
                muted_user = await self.bot.get_guild(main.ids(1)).fetch_member(user.id)
                if role_hierarchy(punisher, muted_user) is True:
                    if self.bot.get_guild(main.ids(1)).get_role(main.ids(12)) in muted_user.roles:
                        await main.error_embed(ctx, 'That member is already muted')
                    else:
                        if mute_time[2] is True:
                            if reason is None and mute_time[0] != 0:
                                await main.error_embed(ctx, 'You need to give a reason')
                            else:
                                await muted_user.add_roles(self.bot.get_guild(main.ids(1)).get_role(main.ids(12)))
                                if mute_time[0] == 0:
                                    reason = '' if reason is None else reason
                                    mute_reason = f'{mute_time[1]} {reason}'
                                    print(mute_reason)
                                    print(mute_time[0])  # this is when there is no time

                                    await main.channel_embed(ctx, 'User Muted', f'{muted_user.mention} has been muted indefinitely for reason: ```{reason}```')
                                    try:  # dm embed
                                        dm_channel = await muted_user.create_dm()
                                        await main.dm_embed('Muted', f'You have been muted in the baritone discord indefinitely for reason: \n```{reason}```', dm_channel)
                                    except (discord.Forbidden, discord.errors.HTTPException):
                                        pass
                                    print(f'{ctx.author.id} muted {muted_user.id} indefinitely for reason: {reason}')  # print message
                                    await main.log_embed(ctx, f'User Muted', f'{muted_user.mention} has been muted indefinitely for reason: ```{reason}```', muted_user)
                                    main.cur.execute('INSERT INTO rekt(user_id, action, expiry, punisher) VALUES(%s, %s, %s, %s)', (muted_user.id, 'muted', int(mute_time[0]), ctx.author.id))
                                    main.db.commit()

                                else:
                                    print(reason)
                                    print(mute_time[0])  # this is when there is a time

                                    await main.channel_embed(ctx, 'User Muted', f'{muted_user.mention} has been muted for {mute_time[1]} for reason: ```{reason}```')
                                    try:  # dm embed
                                        dm_channel = await muted_user.create_dm()
                                        await main.dm_embed('Muted', f'You have been muted in the baritone discord for {mute_time[1]} for reason: \n```{reason}```', dm_channel)
                                    except (discord.Forbidden, discord.errors.HTTPException):
                                        pass
                                    print(f'{ctx.author.id} muted {muted_user.id} for {mute_time[1]} for reason: {reason}')  # print message
                                    await main.log_embed(ctx, f'User Muted', f'{muted_user.mention} has been muted for {mute_time[1]} for reason: ```{reason}```', muted_user)
                                    main.cur.execute('INSERT INTO rekt(user_id, action, expiry, punisher) VALUES(%s, %s, %s, %s)', (muted_user.id, 'muted', int(mute_time[0]), ctx.author.id))
                                    main.db.commit()
                        else:
                            if mute_time[3] == 1:
                                await main.error_embed(ctx, 'Only use `m`(minutes), `h`(hours), or `d`(days).')
                            elif mute_time[3] == 2:
                                await main.error_embed(ctx, 'That time in seconds is larger than 64 bits which isn\'t supported by postgreSQL, please chose a shorter time')
                else:
                    await main.error_embed(ctx, f'You don\'t outrank {muted_user.mention}')
            except discord.NotFound:
                await main.error_embed(ctx, 'That is not a valid member')

    @mute.command(aliases=['l'])
    @commands.check(main.helper_group)
    async def list(self, ctx):
        main.cur.execute("SELECT user_id, expiry FROM rekt WHERE action='muted'")
        muted_users = main.cur.fetchall()
        desc = ''
        for muted_user in muted_users:
            user = self.bot.get_user(muted_user[0])
            remaining = 'indefinite' if muted_user[1] != 0 else main.time_convert(muted_user[1] - int(time()))
            desc += f'**{user} ({user.id}) Time remaining:** \n{remaining}\n'
        await main.channel_embed(ctx, f'Muted Users ({len(muted_users)}):', desc)

    @commands.command(aliases=['k'])
    @commands.check(main.mod_group)
    async def kick(self, ctx):
        pass

    @commands.command()
    async def optout(self, ctx):
        pass


def setup(bot):
    bot.add_cog(Bkm(bot))
