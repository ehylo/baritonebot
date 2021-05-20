import main
import discord
from time import time
from datetime import datetime, timedelta
from discord.ext import commands, tasks


async def unmute_embeds(b_guild, modlog_channel, i):
    if b_guild.get_member(i[0]) is not None:
        try:
            dm_channel = await b_guild.get_member(i[0]).create_dm()
            await main.dm_embed('Unmuted', 'You have been unmuted in the baritone discord', dm_channel)
        except (discord.Forbidden, discord.errors.HTTPException):
            pass
        await main.log_embed(None, 'User Unmuted', f'{b_guild.get_member(i[0]).mention} has been unmuted', modlog_channel, b_guild.get_member(i[0]))
        await b_guild.get_member(i[0]).remove_roles(b_guild.get_role(main.ids(12)))
    print(f'{i[0]} was unmuted automatically')
    main.cur.execute('DELETE FROM rekt WHERE user_id=%s', (i[0],))
    main.db.commit()

main.cur.execute("SELECT ids FROM exempted WHERE type='channel'")
exempt_channels = [str(item[0]) for item in main.cur.fetchall()]
main.cur.execute("SELECT ids FROM exempted WHERE type='user'")
exempt_users = [str(item[0]) for item in main.cur.fetchall()]


class Event(commands.Cog):
    def __init__(self, bot):
        """Returns all of the specific emebeds for even related actions."""
        self.bot = bot
        self.loops.start()

    @commands.Cog.listener()
    async def on_message(self, message):
        if (message.guild is None) and (message.author.id != main.ids(0)) and (str(message.author.id) not in exempt_users):
            channel = self.bot.get_guild(main.ids(1)).get_channel(main.ids(4))
            await main.log_embed(None, 'I have recieved a DM', message.content, channel, message.author)
            print(f'{message.author.id} dmed me \"{message.content}\"')

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if (message.author.id != main.ids(0)) and (str(message.channel.id) not in exempt_channels) and (str(message.author.id) not in exempt_users):
            channel = await self.bot.fetch_channel(main.ids(3))
            if message.guild is None:
                del_channel = 'DMs'
            else:
                del_channel = message.channel.mention
            await main.log_embed(None, None, f'**Message deleted in {del_channel}** \n{message.content}', channel, message.author)
            print(f'{message.author.id} message was deleted: \"{message.content}\"')

    @commands.Cog.listener()
    async def on_message_edit(self, message_before, message_after):
        if message_before.author.id != main.ids(0):
            if (str(message_before.channel.id) not in exempt_channels) and (str(message_after.author.id) not in exempt_users):
                if message_after.content != message_before.content:  # prevent logging embeds loading
                    if message_before.guild is None:
                        jump = 'DMs**'
                    else:
                        jump = f'{message_after.channel.mention}** [(jump)](https://discord.com/channels/{message_after.guild.id}/{message_after.channel.id}/{message_after.id})'
                    em_v = discord.Embed(color=int(main.values(1), 16), description=f'**Message edited in {jump}')
                    em_v.add_field(name='Befored Edit:', value=message_before.content, inline=False)
                    em_v.add_field(name='After Edit:', value=message_after.content, inline=False)
                    em_v.set_footer(text=f'{message_after.author.name} | ID: {message_after.author.id}', icon_url=message_after.author.avatar_url)
                    channel = await self.bot.fetch_channel(main.ids(3))
                    await channel.send(embed=em_v)
                    print(f'{message_after.author.id} edited a message, Before: \"{message_before.content}\" After: \"{message_after.content}\"')

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = await self.bot.fetch_channel(main.ids(2))
        await main.log_embed(None, 'User Left', None, channel, member)
        print(f'{member.id} left the server')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.name.startswith(('!', '"', '#', '$', '%', '&', '\'', '(', ')', '*', '+', ',', '-', '.', '/')):
            await member.edit(nick=f'z{member.name}')
            print(f'{member.id} joined with a name that puts them to the top of the list, so z was added infront')
        channel = await self.bot.fetch_channel(main.ids(2))
        await main.log_embed(None, 'User Joined', None, channel, member)
        main.cur.execute('SELECT user_id FROM rekt WHERE user_id=%s', (member.id,))
        if main.cur.fetchone() is not None:
            await member.add_roles(self.bot.get_guild(main.ids(1)).get_role(main.ids(12)))
            print(f'{member.id} joined the server and was given the mute role because they are still muted')
        else:
            print(f'{member.id} joined the server')

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        try:
            if after.display_name.startswith(('!', '"', '#', '$', '%', '&', '\'', '(', ')', '*', '+', ',', '-', '.', '/')):
                if before.display_name.startswith(('!', '"', '#', '$', '%', '&', '\'', '(', ')', '*', '+', ',', '-', '.', '/')):
                    await after.edit(nick=f'z{after.display_name}')
                    print(f'{after.id} tried to set a nickname to put them at the top of the list so a z was added infront')
                else:
                    await after.edit(nick=before.display_name)
                    print(f'{after.id} tried to set a nickname to put them at the top of the list so it was reverted')
        except discord.Forbidden:
            print(f'{before.id} set a top of the list nick and the bot is missing permissions to change it')

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if before.channel is None:  # only reason its 'before' and 'is' is so that before is used and pycharm stops yelling at me
            b_role = discord.utils.get(member.guild.roles, id=main.ids(14))
            await member.add_roles(b_role)
            print(f'{member.id} joined a voice channel and got the voice role')
        elif after.channel is None:
            b_role = discord.utils.get(member.guild.roles, id=main.ids(14))
            await member.remove_roles(b_role)
            print(f'{member.id} left a voice channel and the voice role was removed')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.errors.UserNotFound):
            await main.error_embed(ctx, 'That member is invalid')
        elif isinstance(error, commands.errors.ChannelNotFound):
            await main.error_embed(ctx, 'That is not a valid channel')
        elif isinstance(error, commands.BadArgument):
            await main.error_embed(ctx, 'You need to give a **number**')
        elif isinstance(error, commands.errors.CommandNotFound):
            await main.error_embed(ctx, f'The command `{ctx.message.content}` was not found, do `help` to see command categories')
        elif not isinstance(error, commands.errors.CheckFailure):
            await main.error_embed(ctx, None, error)
            print(f'{ctx.author.id} tried to use the command {ctx.command} but it gave the error: {error}')

    @tasks.loop(seconds=1)
    async def loops(self):
        b_guild = self.bot.get_guild(main.ids(1))
        modlog_channel = await self.bot.fetch_channel(main.ids(5))
        log_channel = await self.bot.fetch_channel(main.ids(3))
        async for message in log_channel.history(limit=1000):
            if (message.created_at + timedelta(hours=24)) < datetime.utcnow():
                await message.delete()
                print('cleared logs older then 24 hours in the logs channel')
        main.cur.execute('SELECT * FROM rekt')
        now = int(time())
        for i in main.cur.fetchall():
            expiry = i[2]
            if expiry - now <= 0:
                await unmute_embeds(b_guild, modlog_channel, i)


def setup(bot):
    bot.add_cog(Event(bot))
