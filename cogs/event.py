import requests
import re
import mimetypes
import asyncio
import logging
import const
import discord
from datetime import datetime, timedelta
from discord.ext import commands

const.cur.execute('SELECT channel_id FROM ex_channels')
exempt_channels = [str(item[0]) for item in const.cur.fetchall()]
ran_once_yes = False


async def one_min_timer(self):
    global ran_once_yes
    if ran_once_yes is False:
        ran_once_yes = True
        while True:
            await asyncio.sleep(30)
            log_channel = await self.bot.fetch_channel(const.logChannel)
            async for message in log_channel.history(limit=1000):
                if (message.created_at + timedelta(hours=24)) < datetime.utcnow():
                    await message.delete()
                    logging.info('cleared logs older then 24 hours in the logs channel')
            const.cur.execute('SELECT * FROM punish')
            muted = const.cur.fetchall()
            modlog_channel = await self.bot.fetch_channel(const.modlogChannel)
            b_guild = self.bot.get_guild(const.baritoneDiscord)
            for i in muted:
                date_muted = datetime(i[4], i[5], i[6], i[7], i[8])

                async def unmute_embeds():
                    dm_channel = await b_guild.get_member(i[0]).create_dm()
                    logging.info(f'{i[0]} was unmuted automatically')
                    await const.log_embed(None, 'User Unmuted', f'{b_guild.get_member(i[0]).mention} has been unmuted', modlog_channel, b_guild.get_member(i[0]))
                    await const.dm_embed('Unmuted', 'You have been unmuted in the baritone discord', dm_channel)
                    await b_guild.get_member(i[0]).remove_roles(b_guild.get_role(const.muteRole))
                    const.cur.execute('DELETE FROM punish WHERE user_id=%s', (i[0],))
                    const.db.commit()
                if i[2].lower() == 'm':
                    if (date_muted + timedelta(minutes=i[1])) <= datetime.utcnow():
                        await unmute_embeds()
                elif i[2].lower() == 'h':
                    if (date_muted + timedelta(hours=i[1])) <= datetime.utcnow():
                        await unmute_embeds()
                elif i[2].lower() == 'd':
                    if (date_muted + timedelta(days=i[1])) <= datetime.utcnow():
                        await unmute_embeds()


async def del_blacklist(message, b_guild):
    del_message = 0
    if del_message == 0:
        if (not message.content.startswith(const.values[0]) and                     # don't delete commands
                message.guild is not None and                                 # don't try to delete dm messages
                message.author.id is not const.botID and                            # don't delete messages from itself
                str(message.channel.id) not in exempt_channels):              # don't delete messages in exempted channels
            if re.search(r'(https?://)?(www.)?(discord.(gg|io|me|li)|discordapp.com/invite)/[^\s/]+?(?=\b)', message.content) is not None:
                await message.delete()
                dchannel = await message.author.create_dm()
                await const.dm_embed('Message Deleted', f'Your message in {message.channel.mention} was deleted because sending invite links is against the rules', dchannel)
                logging.info(f'{message.author.id} tried to send an invite link but it was deleted')
            else:
                const.cur.execute('SELECT blacklist_word FROM blacklist')
                blacklist_list = const.cur.fetchall()
                for x in range(1, (len(blacklist_list) + 1)):
                    if re.search(blacklist_list[x - 1][0], message.content) is not None:
                        deleted_word = ''
                        try:
                            await message.delete()
                            first_deleted_word = f'{blacklist_list[x - 1][0]}'
                            del_message += 1
                        except discord.NotFound:
                            deleted_word += f'`, `{blacklist_list[x - 1][0]}'
                if del_message > 0:
                    try:
                        dchannel = await message.author.create_dm()
                        await const.dm_embed('Message Deleted', f'Your message in {message.channel.mention} was deleted because `{first_deleted_word}{deleted_word}` is blacklisted', dchannel)
                    except discord.Forbidden:
                        pass
                    logging.info(f'{message.author.id} sent a message but it was deleted because it has a word on the blacklist')
    if del_message == 0:
        await att_paste(message)
        await dm_log(message, b_guild)
        await gexre(message, b_guild)


async def dm_log(message, b_guild):
    if (message.guild is None) and (message.author.id != const.botID):
        channel = b_guild.get_channel(const.dmChannel)
        await const.log_embed(message, f'I have recieved a DM', message.content, channel, None)
        logging.info(f'{message.author.id} dmed me \"{message.content}\"')


async def att_paste(message):
    if len(message.attachments) > 0:
        file_type = mimetypes.guess_type(message.attachments[0].url)
        if file_type[0] is not None:
            file_type = file_type[0].split('/')[0]
        if message.attachments[0].url.lower().endswith(('.log', '.json5', '.json', '.py', '.sh', '.config', '.properties', '.toml', '.bat', '.cfg')) or file_type == 'text':
            text = await discord.Attachment.read(message.attachments[0], use_cached=False)
            paste_response = requests.post(url='https://api.paste.ee/v1/pastes', json={'sections': [{'name': "Paste from " + str(message.author), 'contents': ("\n".join((text.decode('UTF-8')).splitlines()))}]}, headers={'X-Auth-Token': const.pasteToken})
            actual_link = paste_response.json()
            await const.channel_embed(message.channel, 'Contents uploaded to paste.ee', (actual_link["link"]))
            logging.info(f'{message.author.id} uploaded a paste to {(actual_link["link"])}')


async def gexre(message, b_guild):
    if (not message.content.startswith(const.values[0])) and (message.author.id != const.botID):
        const.cur.execute('SELECT * FROM responses')
        response_list = const.cur.fetchall()
        for x in range(1, (len(response_list) + 1)):
            if re.search(response_list[x-1][0], message.content) is not None:
                member = await b_guild.fetch_member(message.author.id)
                if (b_guild.get_member(const.botID) in message.mentions) or (message.content.startswith('!')):  # this is seperate from the elif so there is no trash reaction to delete a pinged/command response, and also the bot won't reply
                    await const.channel_embed(message.channel, (response_list[x-1][1]), (response_list[x-1][2]))
                    logging.info(f'{message.author.id} manually triggered response number {x}')
                    # await message.delete()  # might add this, need to ask people first
                elif (b_guild.get_role(const.ignoreRole) not in member.roles) and (str(message.channel.id) not in exempt_channels):
                    await const.channel_embed(message, (response_list[x-1][1]), (response_list[x-1][2]), None, 'Reply')
                    logging.info(f'{message.author.id} sent a message and triggered response number {x}')


class Event(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await one_min_timer(self)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.id != const.botID and str(message.channel.id) not in exempt_channels:
            channel = await self.bot.fetch_channel(const.logChannel)
            if message.guild is None:
                del_channel = 'DMs'
            else:
                del_channel = message.channel.mention
            await const.log_embed(message, None, f'**Message deleted in {del_channel}** \n{message.content}', channel)
            logging.info(f'{message.author.id} message was deleted: \"{message.content}\"')

    @commands.Cog.listener()
    async def on_message_edit(self, message_before, message_after):
        if message_before.author.id != const.botID:
            if str(message_before.channel.id) not in exempt_channels:
                if message_after.content != message_before.content:  # prevent logging embeds loading
                    if message_before.guild is None:
                        jump = 'DMs**'
                    else:
                        jump = f'{message_after.channel.mention}** [(jump)](https://discord.com/channels/{message_after.guild.id}/{message_after.channel.id}/{message_after.id})'
                    em_v = discord.Embed(color=const.coolEmbedColor, timestamp=datetime.utcnow(), description=f'**Message edited in {jump}')
                    em_v.add_field(name='Befored Edit:', value=message_before.content, inline=False)
                    em_v.add_field(name='After Edit:', value=message_after.content, inline=False)
                    em_v.set_author(name=message_after.author, icon_url=message_after.author.avatar_url)
                    em_v.set_footer(text=f'\U0001f916 Baritone Bot \U0001f916 ID: {message_after.author.id}')
                    channel = await self.bot.fetch_channel(const.logChannel)
                    await channel.send(embed=em_v)
                    logging.info(f'{message_after.author.id} edited a message, Before: \"{message_before.content}\" After: \"{message_after.content}\"')
        await del_blacklist(message_after, b_guild=self.bot.get_guild(const.baritoneDiscord))

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = await self.bot.fetch_channel(const.leaveChannel)
        await const.log_embed(None, 'User Left', None, channel, member)
        logging.info(f'{member.id} left the server')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.name.startswith(('!', '"', '#', '$', '%', '&', '\'', '(', ')', '*', '+', ',', '-', '.', '/')):
            await member.edit(nick=f'z{member.name}')
            logging.info(f'{member.id} joined with a name that puts them to the top of the list, so z was added infront')
        channel = await self.bot.fetch_channel(const.leaveChannel)
        await const.log_embed(None, 'User Joined', None, channel, member)
        logging.info(f'{member.id} joined the server')

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        try:
            if after.display_name.startswith(('!', '"', '#', '$', '%', '&', '\'', '(', ')', '*', '+', ',', '-', '.', '/')):
                if before.display_name.startswith(('!', '"', '#', '$', '%', '&', '\'', '(', ')', '*', '+', ',', '-', '.', '/')):
                    await after.edit(nick=f'z{after.display_name}')
                    logging.info(f'{after.id} tried to set a nickname to put them at the top of the list so a z was added infront')
                else:
                    await after.edit(nick=before.display_name)
                    logging.info(f'{after.id} tried to set a nickname to put them at the top of the list so it was reverted')
        except discord.Forbidden:
            logging.error(f'{before.id} set a top of the list nick and the bot is missing permissions to change it')

    @commands.Cog.listener()
    async def on_message(self, message):
        await del_blacklist(message, b_guild=self.bot.get_guild(const.baritoneDiscord))
    # await self.bot.process_commands(message)  # commenting this out because it didn't work at one point without it but now if enabled it sends 2 messages idfk just leave it why not

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if before.channel is None:  # only reason its 'before' and 'is' is so that before is used and pycharm stops yelling at me
            b_role = discord.utils.get(member.guild.roles, id=const.voiceRole)
            await member.add_roles(b_role)
            logging.info(f'{member.id} joined a voice channel and got the voice role')
        elif after.channel is None:
            b_role = discord.utils.get(member.guild.roles, id=const.voiceRole)
            await member.remove_roles(b_role)
            logging.info(f'{member.id} left a voice channel and the voice role was removed')

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        message = reaction.message
        if reaction.emoji == '🗑️':  # make sure the reaction is the wastebasket
            if (message.author.id == const.botID) and (user.id != const.botID):  # make sure the bot sent the message and it wasn't the one who reacted
                helper_role = self.bot.get_guild(const.baritoneDiscord).get_role(const.helperRole)
                try:
                    reaction_trigger = await message.channel.fetch_message(message.reference.message_id)
                    if (user.id == reaction_trigger.author.id) or (helper_role in user.roles):  # delete if the person is a helper or they were the ones who triggered it
                        await message.delete()
                except AttributeError:  # to stop errors if people use this in dms
                    pass

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.errors.UserNotFound):
            await const.error_embed(ctx, 'That member is invalid')
        elif isinstance(error, commands.BadArgument):
            await const.error_embed(ctx, 'You need to give a **number**')
        elif isinstance(error, commands.errors.CommandNotFound):
            await const.error_embed(ctx, f'The command `{ctx.message.content}` was not found, do `help` to see command categories')
        elif not isinstance(error, commands.errors.CheckFailure):
            await const.error_embed(ctx, None, error)
            logging.error(f'{ctx.author.id} tried to use the command {ctx.command} but it gave the error: {error}')


def setup(bot):
    bot.add_cog(Event(bot))
