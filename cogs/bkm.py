import discord
import main
from time import time
from cogs.help import Help
from discord.ext import commands


async def member_check(self, ctx, user):
    return await self.bot.get_guild(main.ids(1)).fetch_member(user.id), await self.bot.get_guild(main.ids(1)).fetch_member(ctx.author.id)


async def output(member, action, channel, time_muted, ctx, reason, log_e=None):
    print(f'{ctx.author.id} {action} {member.id}{time_muted} {reason}')
    await main.log_embed(log_e, f'User {action.capitalize()}', f'{member.mention} has been {action}{time_muted} {reason}', channel, member)
    await main.channel_embed(ctx, f'User {action.capitalize()}', f'{member.mention} has been {action}{time_muted} {reason}')


class Bkm(commands.Cog):
    def __init__(self, bot):
        """Returns embeds for all the punishment commands."""
        self.bot = bot

    @commands.command(aliases=['ub'])
    @commands.check(main.mod_group)
    async def unban(self, ctx, user=None):
        try:
            user_men = str(ctx.message.raw_mentions[0])
        except IndexError:
            user_men = ''
        b_guild = self.bot.get_guild(main.ids(1))
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
                await main.error_embed(ctx, 'The user you gave is invalid')
            else:
                try:
                    user = await self.bot.fetch_user(user)
                    await b_guild.unban(unban_user)
                    channel = await self.bot.fetch_channel(main.ids(5))
                    await output(user, 'unbanned', channel, '', ctx, '', None)
                except discord.NotFound:
                    await main.error_embed(ctx, 'That user is not banned')

    @commands.command(aliases=['um'])
    @commands.check(main.mod_group)
    async def unmute(self, ctx, user: discord.User = None):
        member, author_member = await member_check(self, ctx, user)
        if member is None:
            await Help.unmute(self, ctx)
        elif member.top_role == author_member.top_role:
            await main.error_embed(ctx, f'You don\'t outrank {member.mention}')
        else:
            if self.bot.get_guild(main.ids(1)).get_role(main.ids(12)) not in member.roles:
                await main.error_embed(ctx, 'That member is not muted')
            else:
                await member.remove_roles(self.bot.get_guild(main.ids(1)).get_role(main.ids(12)))
                try:
                    dm_channel = await member.create_dm()
                    await main.dm_embed('Unmuted', 'You have been unmuted in the baritone discord', dm_channel)
                except (discord.Forbidden, discord.errors.HTTPException):
                    pass
                channel = await self.bot.fetch_channel(main.ids(5))
                await output(member, 'unmuted', channel, '', ctx, '', ctx)
                main.cur.execute('DELETE FROM rekt WHERE user_id=%s', (user.id,))
                main.db.commit()

    @commands.command(aliases=['b', 'rm'])
    @commands.check(main.mod_group)
    async def ban(self, ctx, user: discord.User = None, purge=None, *, reason=None):
        member, author_member = await member_check(self, ctx, user)
        if member is None:
            await Help.ban(self, ctx)
        elif member.top_role == author_member.top_role:
            await main.error_embed(ctx, f'You don\'t outrank {member.mention}')
        elif purge is None:
            await main.error_embed(ctx, 'You need to give a reason')
        else:
            async def ban_embeds(reasons):
                try:
                    dm_channel = await member.create_dm()
                    await main.dm_embed('Banned', f'You have been banned from the baritone discord for reason: \n```{reasons}```', dm_channel)
                except (discord.Forbidden, discord.errors.HTTPException):
                    pass
                channel = await self.bot.fetch_channel(main.ids(5))
                await output(member, 'banned', channel, '', ctx, f'for reason: \n```{reasons}```', ctx)
            if purge.lower() == 'purge':
                await ban_embeds(reason)
                await member.ban(reason=reason, delete_message_days=7)
            else:
                await ban_embeds(f'{purge} {reason}')
                await member.ban(reason=reason, delete_message_days=0)

    @commands.group(invoke_without_command=True, case_insensitive=True, aliases=['m'])
    @commands.check(main.helper_group)
    async def mute(self, ctx, user: discord.User = None, mtime=None, *, reason=None):
        member, author_member = await member_check(self, ctx, user)
        if member is None:
            await Help.mute(self, ctx)
        elif member.top_role == author_member.top_role:
            await main.error_embed(ctx, f'You don\'t outrank {member.mention}')
        elif mtime is None:
            await main.error_embed(ctx, 'You need to give a reason or amount of time to mute')
        elif (mtime[0].isdigit()) and (reason is None) and (''.join(i for i in mtime if not i.isdigit()) == ''):
            await main.error_embed(ctx, 'You need to give a reason')
        else:
            if self.bot.get_guild(main.ids(1)).get_role(main.ids(12)) in member.roles:
                await main.error_embed(ctx, 'That member is already muted')
            else:
                if reason is None:
                    reason = ''

                async def mute_embeds(time_muted, expiry, ereason):
                    await member.add_roles(self.bot.get_guild(main.ids(1)).get_role(main.ids(12)))
                    try:
                        dm_channel = await member.create_dm()
                        await main.dm_embed('Muted', f'You have been muted in the baritone discord {time_muted}, reason: \n```{ereason}```', dm_channel)
                    except (discord.Forbidden, discord.errors.HTTPException):
                        pass
                    channel = await self.bot.fetch_channel(main.ids(5))
                    await output(member, 'muted', channel, f' for {time_muted}', ctx, f'for reason: \n```{ereason}```', ctx)
                    main.cur.execute('INSERT INTO rekt(user_id, action, expiry) VALUES(%s, %s, %s)', (member.id, 'muted', expiry))
                    main.db.commit()
                x = int(time())
                if mtime[0].isdigit():
                    multiply = ''.join(i for i in mtime if not i.isdigit())
                    amount = ''.join(i for i in mtime if i.isdigit())
                    if multiply == '':
                        await mute_embeds('indefinitely', '0', f'{mtime} {reason}')
                    elif (len(multiply) > 1) or ((multiply.lower() != 'm') and (multiply.lower() != 'd') and (multiply.lower() != 'h')):
                        await main.error_embed(ctx, "Only use `m`(minutes), `h`(hours), or `d`(days).")
                    else:
                        if multiply.lower() == 'd':
                            x += (int(amount) * 24 * 60 * 60)
                        elif multiply.lower() == 'h':
                            x += (int(amount) * 60 * 60)
                        elif multiply.lower() == 'm':
                            x += (int(amount) * 60)
                        await mute_embeds(f'for {mtime}', x, reason)
                else:
                    await mute_embeds('indefinitely', '0', f'{mtime} {reason}')

    @mute.command(aliases=['l'])
    @commands.check(main.helper_group)
    async def list(self, ctx):
        main.cur.execute("SELECT user_id, expiry FROM rekt WHERE action='muted'")
        muted_users = main.cur.fetchall()
        desc = ''
        for row in muted_users:
            if row[1] != 0:
                edesc = ''
                expiry = new = (row[1] - int(time()))
                if expiry / 86400 >= 1:
                    edesc += f', {(expiry - (expiry % 86400)) // 86400} day(s)'
                    new = expiry - ((expiry - (expiry % 86400)) // 86400 * 86400)
                if new / 3600 >= 1:
                    edesc += f', {(new - (new % 3600)) // 3600} hour(s)'
                    new -= ((new - (new % 3600)) // 3600 * 3600)
                if new / 60 >= 1:
                    edesc += f', {(new - (new % 60)) // 60} minute(s)'
                    new -= ((new - (new % 60)) // 60 * 60)
                if new >= 1:
                    edesc += f', {new} second(s)'
                desc += f'**<@{row[0]}> Time remaining:** \n{edesc[2:]}\n'
            else:
                desc += f'**<@{row[0]}> Time remaining:** \nindefinite\n'
        await main.channel_embed(ctx, f'Muted Users ({len(muted_users)}):', desc)

    @commands.command(aliases=['k'])
    @commands.check(main.mod_group)
    async def kick(self, ctx, user: discord.User = None, *, reason=None):
        member, author_member = await member_check(self, ctx, user)
        if member is None:
            await Help.kick(self, ctx)
        elif member.top_role == author_member.top_role:
            await main.error_embed(ctx, f'You don\'t outrank {member.mention}')
        elif reason is None:
            await main.error_embed(ctx, 'You need to give a reason')
        else:
            try:
                dm_channel = await member.create_dm()
                await main.dm_embed('Kicked', f'You have been kicked from the baritone discord for reason: \n```{reason}```', dm_channel)
            except (discord.Forbidden, discord.errors.HTTPException):
                pass
            channel = await self.bot.fetch_channel(main.ids(5))
            await output(member, 'kicked', channel, '', ctx, f'for reason: \n```{reason}```', ctx)
            await member.kick(reason=reason)


def setup(bot):
    bot.add_cog(Bkm(bot))
