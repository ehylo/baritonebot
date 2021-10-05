import main
import discord
from time import time
from datetime import datetime, timedelta
from discord.ext import commands, tasks


async def unmute_embeds(b_guild, modlog_channel, i):
    class RektAuthor:
        author = b_guild.get_member(i[3])
    if b_guild.get_member(i[0]) is not None:
        try:
            dm_channel = await b_guild.get_member(i[0]).create_dm()
            await main.dm_embed('Unmuted', 'You have been unmuted in the baritone discord', dm_channel)
        except (discord.Forbidden, discord.errors.HTTPException):
            pass
        await main.log_embed(RektAuthor(), 'User Unmuted', f'{b_guild.get_member(i[0]).mention} has been unmuted', modlog_channel, b_guild.get_member(i[0]))
        await b_guild.get_member(i[0]).remove_roles(b_guild.get_role(main.ids(12)))
    print(f'{i[0]} was unmuted automatically')
    main.cur.execute('DELETE FROM rekt WHERE user_id=%s', (i[0],))
    main.db.commit()


async def unhoist(member):

    def name_loop(name):
        if name.startswith(hoisted_list):
            return name_loop(name[1:])
        if name == '':
            return 'z' + member.name
        return name
    await member.edit(nick=name_loop(member.name))
    print(f'{member.id} tried to set a nickname to put them at the top of the list but the hoisted char. was removed')

main.cur.execute("SELECT ids FROM exempted WHERE type='channel'")
exempt_channels = [str(item[0]) for item in main.cur.fetchall()]
hoisted_list = ('!', '"', '#', '$', '%', '&', '\'', '(', ')', '*', '+', ',', '-', '.', '/')


class Event(commands.Cog):
    def __init__(self, bot):
        """Returns all of the specific emebeds for even related actions."""
        self.bot = bot
        self.loops.start()

    def cog_unload(self):
        self.loops.cancel()

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.discriminator != '0000':
            if (message.author.id != main.ids(0)) and (str(message.channel.id) not in exempt_channels):
                if message.guild is not None:
                    channel = await self.bot.get_channel(main.ids(3))
                    del_channel = message.channel.mention
                    await main.log_embed(None, None, f'**Message deleted in {del_channel}** \n{message.content}', channel, message.author)
                    print(f'{message.author.id} message was deleted: \"{message.content}\"')

    @commands.Cog.listener()
    async def on_message_edit(self, message_before, message_after):
        if message_after.author.discriminator != '0000':
            if message_after.content != '' and message_before.content != '':
                if message_before.author.id != main.ids(0):
                    if str(message_before.channel.id) not in exempt_channels:
                        if message_after.content != message_before.content:
                            if message_before.guild is not None:
                                jump = f'{message_after.channel.mention}** [(jump)](https://discord.com/channels/{message_after.guild.id}/{message_after.channel.id}/{message_after.id})'
                                em_v = discord.Embed(color=int(main.values(1), 16), description=f'**Message edited in {jump}')
                                em_v.add_field(name='Befored Edit:', value=message_before.content, inline=False)
                                em_v.add_field(name='After Edit:', value=message_after.content, inline=False)
                                em_v.set_footer(text=f'{message_after.author.name} | ID: {message_after.author.id}', icon_url=message_after.author.avatar_url)
                                channel = await self.bot.get_channel(main.ids(3))
                                await channel.send(embed=em_v)
                                print(f'{message_after.author.id} edited a message, Before: \"{message_before.content}\" After: \"{message_after.content}\"')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.name.startswith(hoisted_list):
            await unhoist(member)
        main.cur.execute('SELECT user_id FROM rekt WHERE user_id=%s', (member.id,))
        if main.cur.fetchone() is not None:
            await member.add_roles(self.bot.get_guild(main.ids(1)).get_role(main.ids(12)))
            print(f'{member.id} joined the server and was given the mute role because they are still muted')

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        try:
            if after.display_name.startswith(hoisted_list):
                if before.display_name.startswith(hoisted_list):
                    await unhoist(after)
                else:
                    await after.edit(nick=before.display_name)
                    print(f'{after.id} tried to set a nickname to put them at the top of the list so it was reverted')
        except discord.Forbidden:
            print(f'{before.id} set a top of the list nick and the bot is missing permissions to change it')

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if before.channel is None:
            if self.bot.get_guild(main.ids(1)).get_role(main.ids(14)) not in member.roles:
                await member.add_roles(self.bot.get_guild(main.ids(1)).get_role(main.ids(14)))
            print(f'{member.id} joined a voice channel and got the voice role')
        elif after.channel is None:
            if self.bot.get_guild(main.ids(1)).get_role(main.ids(14)) in member.roles:
                await member.remove_roles(self.bot.get_guild(main.ids(1)).get_role(main.ids(14)))
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
        elif isinstance(error, commands.errors.CheckFailure):
            pass

    @tasks.loop(seconds=1)
    async def loops(self):
        log_channel = await self.bot.get_channel(main.ids(3))
        async for message in log_channel.history(limit=1000):
            if (message.created_at + timedelta(hours=24)) < datetime.utcnow():
                await message.delete()
                print('cleared logs older then 24 hours in the logs channel')
        main.cur.execute('SELECT * FROM rekt')
        for i in main.cur.fetchall():
            if i[2] != 0:
                if i[2]-int(time()) <= 0:
                    await unmute_embeds(self.bot.get_guild(main.ids(1)), await self.bot.get_channel(main.ids(5)), i)

    @loops.before_loop
    async def before_loops(self):
        print('[STARTUP] waiting to start loops...')
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(Event(bot))
