import main
import re
import discord
import mimetypes
import requests
import asyncio
from discord.ext import commands
from cogs.help import Help


def staffr_check(self, mmember):
    for x in [main.ids(8), main.ids(10), main.ids(7), main.ids(9), main.ids(6)]:
        if self.bot.get_guild(main.ids(1)).get_role(x) in self.bot.get_guild(main.ids(1)).get_member(mmember).roles:
            return True


def role_check(self, member, ig_roles):
    for y in ig_roles.strip('}{').split(','):
        if self.bot.get_guild(main.ids(1)).get_role(int(y)) in member.roles:
            return True


async def regex_delete(self, message):
    if (not message.content.lower().startswith(main.values(0)) and
            message.author.id != main.ids(0) and
            staffr_check(self, message.author.id) is not True):
        main.cur.execute('SELECT * FROM response WHERE delete=true')
        match_regex = main.cur.fetchall()
        for x in match_regex:
            if re.search(x[0], message.content) is not None:
                try:
                    await main.dm_embed(x[1], x[2], await message.author.create_dm())
                    await message.delete()
                except (discord.NotFound, discord.Forbidden, discord.errors.HTTPException):
                    pass
                print(f'{message.author.id} sent a message but it was deleted because it matched response #{x[5]}')
                return True


async def regex_respond(self, message):
    b_guild = self.bot.get_guild(main.ids(1))
    if not message.content.lower().startswith(main.values(0)) and message.author.id != main.ids(0):
        main.cur.execute('SELECT * FROM response WHERE delete=false')
        match_regex = main.cur.fetchall()
        for x in match_regex:
            if re.search(x[0], message.content) is not None:
                member = b_guild.get_member(message.author.id)
                if (b_guild.get_member(main.ids(0)) in message.mentions) or (message.content.startswith('!')):
                    await main.channel_embed(message.channel, (x[1]), (x[2]))
                    print(f'{message.author.id} manually triggered response #{x[5]}')
                    await message.delete()
                elif role_check(self, member, x[4]) is not True:
                    print(f'{message.author.id} triggered response #{x[5]}')
                    em_v = discord.Embed(color=int(main.values(1), 16), title=x[1], description=x[2])
                    em_v.set_footer(text=f'{message.author.name} | ID: {message.author.id}', icon_url=message.author.avatar_url)
                    auto_response = await message.channel.send(embed=em_v)
                    await auto_response.add_reaction('🗑️')

                    def check(dreaction, duser):
                        try:
                            return (auto_response == dreaction.message) and (duser.id == message.author.id or staffr_check(self, duser.id) is True)
                        except AttributeError:
                            pass

                    while True:
                        try:
                            reaction, user = await self.bot.wait_for('reaction_add', timeout=1800, check=check)
                        except asyncio.TimeoutError:
                            break
                        else:
                            if str(reaction) == '🗑️' and user.id != int(main.ids(0)):
                                try:
                                    await auto_response.delete()
                                except AttributeError:
                                    pass
                                break


async def att_paste(message):
    if len(message.attachments) > 0:
        file_type = mimetypes.guess_type(message.attachments[0].url)
        if file_type[0] is not None:
            file_type = file_type[0].split('/')[0]
        if message.attachments[0].url.lower().endswith(('.log', '.json5', '.json', '.py', '.sh', '.config', '.properties', '.toml', '.bat', '.cfg')) or file_type == 'text':
            text = await discord.Attachment.read(message.attachments[0], use_cached=False)
            paste_response = requests.post(url='https://api.paste.ee/v1/pastes', json={'sections': [{'name': "Paste from " + str(message.author), 'contents': ("\n".join((text.decode('UTF-8')).splitlines()))}]}, headers={'X-Auth-Token': main.pasteToken})
            actual_link = paste_response.json()
            await main.channel_embed(message, 'Contents uploaded to paste.ee', (actual_link["link"]))
            print(f'{message.author.id} uploaded a paste to {(actual_link["link"])}')


async def cancel_new(ctx, what, arep_num, dontdelete=None):
    if dontdelete is None:
        main.cur.execute('DELETE FROM response WHERE rep_number=%s', (arep_num,))
        main.db.commit()
        print(f'{ctx.author.id} canceled the new response #{arep_num}')
    else:
        what = 'Edit was canceled because it has been an hour with no response'
    await main.error_embed(ctx, what, None, 'Canceled')


async def ig_what(ctx, message, arep_num, dontdelete):
    if message.content != 'cancel':
        if message.content != 'none':
            main.cur.execute('UPDATE response SET ig_roles = %s WHERE rep_number=%s', (list(message.content.split(" ")), arep_num))
        else:
            main.cur.execute("UPDATE response SET ig_roles='{}' WHERE rep_number=%s", (arep_num,))
        main.db.commit()
        await message.add_reaction('✅')
        return True
    await cancel_new(ctx, 'no', arep_num, dontdelete)


async def text_what(ctx, message, what, arep_num, dontdelete):
    if message.content != 'cancel':
        if what == 'title':
            main.cur.execute('UPDATE response SET title = %s WHERE rep_number=%s', (message.content, arep_num))
        elif what == 'description':
            main.cur.execute('UPDATE response SET description = %s WHERE rep_number=%s', (message.content, arep_num))
        elif what == 'regex':
            main.cur.execute('UPDATE response SET regex = %s WHERE rep_number=%s', (message.content, arep_num))
        main.db.commit()
        await message.add_reaction('✅')
        return True
    await cancel_new(ctx, 'no', arep_num, dontdelete)


async def what_text(self, ctx, what, arep_num, desc, dontdelete=None):
    em_v = discord.Embed(color=int(main.values(1), 16), description=desc)
    em_v.set_footer(text=f'{ctx.author.name} | ID: {ctx.author.id}', icon_url=ctx.author.avatar_url)
    bot_text = await ctx.send(embed=em_v)

    def check(m):
        try:
            return bot_text.id == m.reference.message_id and m.author.id == ctx.author.id
        except AttributeError:
            pass
    while True:
        try:
            message = await self.bot.wait_for('message', timeout=3600, check=check)
        except asyncio.TimeoutError:
            return await cancel_new(ctx, 'The new response was deleted because an hour has passed with no response', arep_num, dontdelete)
        else:
            if 'none' in desc:
                if await ig_what(ctx, message, arep_num, dontdelete) is True:
                    return True
                break
            else:
                if await text_what(ctx, message, what, arep_num, dontdelete) is True:
                    return True
                break


async def do_delete(self, ctx, arep_num, dontdelete=None):
    em_v = discord.Embed(color=int(main.values(1), 16), description=' \
        Do you want this to delete the message if it matches the regex? \
        \n\u2022 🟢 for yes \
        \n\u2022 🔴 for no \
        \n\u2022 ❌ to cancel')
    em_v.set_footer(text=f'{ctx.author.name} | ID: {ctx.author.id}', icon_url=ctx.author.avatar_url)
    bot_delete = await ctx.send(embed=em_v)
    for i in ['🟢', '🔴', '❌']:
        await bot_delete.add_reaction(i)

    def check(dreaction, duser):
        try:
            return bot_delete.id == dreaction.message.id and duser.id == ctx.author.id
        except AttributeError:
            pass
    while True:
        try:
            reaction = await self.bot.wait_for('reaction_add', timeout=300, check=check)
        except asyncio.TimeoutError:
            return await cancel_new(ctx, 'The new response was deleted because 5 minutes has passed with no reaction', arep_num, dontdelete)
        else:
            if str(reaction) == '🟢':  # green circle emote
                main.cur.execute('UPDATE response SET delete=true WHERE rep_number=%s', (arep_num,))
                main.db.commit()
                return True
            if str(reaction) == '🔴':  # red circle emote
                main.cur.execute('UPDATE response SET delete=false WHERE rep_number=%s', (arep_num,))
                main.db.commit()
                return True
            if str(reaction) == '❌':
                await cancel_new(ctx, 'no', arep_num, dontdelete)
                break

title_desc = 'Please reply to this message with the title for this response \n\u2022 reply with `cancel` to cancel'
desc_desc = 'Please reply to this message with the description for this response \n\u2022 reply with `cancel` to cancel'
regex_desc = 'Please reply to this message with the regex for this response \n\u2022 reply with `cancel` to cancel'
ignorerole_desc = 'Please reply with the ids of the roles to be ignored from this response, seperated by a space for muliple \n\u2022 reply with `none` for no ignored roles \n\u2022 reply with `cancel` to cancel'


class Response(commands.Cog):
    def __init__(self, bot):
        """Returns embeds and has listeners for events for all of the response commands."""
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if await regex_delete(self, message) is not True:
            await regex_respond(self, message)
            await att_paste(message)

    @commands.Cog.listener()
    async def on_message_edit(self, message_before, message_after):
        if message_before.content != message_after.content:
            await regex_delete(self, message_after)

    @commands.group(invoke_without_command=True, case_insensitive=True, aliases=['rp'])
    @commands.check(main.helper_group)
    async def response(self, ctx):
        await Help.response(self, ctx)

    @response.command(aliases=['n'])
    @commands.check(main.mod_group)
    async def new(self, ctx):
        main.cur.execute('SELECT rep_number FROM response ORDER BY rep_number')
        rep_nums = main.cur.fetchall()
        arep_num = 1
        for i in [int(item[0]) for item in rep_nums]:
            if arep_num == i:
                arep_num += 1
        main.cur.execute('INSERT INTO response(rep_number) VALUES(%s)', (arep_num,))
        main.db.commit()
        print(f'{ctx.author.id} created a new response #{arep_num}')
        if await what_text(self, ctx, 'title', arep_num, title_desc) is True:
            if await what_text(self, ctx, 'description', arep_num, desc_desc) is True:
                if await what_text(self, ctx, 'regex', arep_num, regex_desc) is True:
                    if await do_delete(self, ctx, arep_num) is True:
                        if await what_text(self, ctx, 'ignoreroles', arep_num, ignorerole_desc) is True:
                            await main.channel_embed(ctx, 'Success!', f'To view the details of this new response, do `{main.values(0)}response details {arep_num}`')

    @response.command(aliases=['e'])
    @commands.check(main.mod_group)
    async def edit(self, ctx, num: int = None):
        if num is None:
            return await main.error_embed(ctx, 'You need to give a response number to edit')
        if num <= 0:
            return await main.error_embed(ctx, 'You need to give a **positive non zero** number')
        main.cur.execute('SELECT * FROM response WHERE rep_number=%s', (num,))
        response = main.cur.fetchone()
        if response is not None:
            em_v = discord.Embed(color=int(main.values(1), 16), title='What would you like to edit?', description=' \
              \u2022 :one: The title \
              \n\u2022 :two: The description \
              \n\u2022 :three: The regex \
              \n\u2022 :four: Delete the message or not \
              \n\u2022 :five: Ignored roles')
            em_v.set_footer(text=f'{ctx.author.name} | ID: {ctx.author.id}', icon_url=ctx.author.avatar_url)
            bot_edit = await ctx.send(embed=em_v)
            for i in ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣']:
                await bot_edit.add_reaction(i)

            def check(ereaction, euser):
                return bot_edit.id == ereaction.message.id and euser.id == ctx.author.id

            while True:
                try:
                    reaction = await self.bot.wait_for('reaction_add', timeout=300, check=check)
                except asyncio.TimeoutError:
                    return await main.error_embed(ctx, '', num, 'don\'t delete')
                else:
                    if str(reaction) == '1️⃣':
                        return await what_text(self, ctx, 'title', num, title_desc, 'don\'t delete')
                    if str(reaction) == '2️⃣':
                        return await what_text(self, ctx, 'description', num, desc_desc, 'don\'t delete')
                    if str(reaction) == '3️⃣':
                        return await what_text(self, ctx, 'regex', num, regex_desc, 'don\'t delete')
                    if str(reaction) == '4️⃣':
                        return await do_delete(self, ctx, num, 'don\'t delete')
                    if str(reaction) == '5️⃣':
                        return await what_text(self, ctx, 'ignore', num, ignorerole_desc, 'don\'t delete')
                    print(f'{ctx.author.id} edited response #{num}')
        else:
            await main.error_embed(ctx, 'There is no response with that number')

    @response.command(aliases=['r'])
    @commands.check(main.mod_group)
    async def remove(self, ctx, num: int = None):
        if num is None:
            return await main.error_embed(ctx, 'You need to give a response number to remove')
        if num <= 0:
            return await main.error_embed(ctx, 'You need to give a **positive non zero** number')
        main.cur.execute('SELECT * FROM response WHERE rep_number=%s', (num,))
        response = main.cur.fetchone()
        if response is not None:
            await main.channel_embed(ctx, f'Removed response #{num}:', response[1])
            print(f'{ctx.author.id} removed response #{num}, \"{response[1]}\"')
            main.cur.execute('DELETE FROM response WHERE rep_number=%s', (num,))
            main.db.commit()
        else:
            await main.error_embed(ctx, 'There is no response with that number')

    @response.command(aliases=['l'])
    @commands.check(main.helper_group)
    async def list(self, ctx):
        main.cur.execute('SELECT ROW_NUMBER () OVER ( ORDER BY rep_number ) rownum, * FROM response')
        responses = main.cur.fetchall()
        desc = ''
        for row in responses:
            desc += f'**{row[6]}.** {row[2]}\n'
        await main.channel_embed(ctx, f'Current Responses ({len(responses)}):', desc)

    @response.command(aliases=['d'])
    @commands.check(main.helper_group)
    async def details(self, ctx, num: int = None):
        if num is None:
            return await main.error_embed(ctx, 'You need to give the response number to get the details')
        if num <= 0:
            return await main.error_embed(ctx, 'You need to give a **positive non zero** response number')
        main.cur.execute('SELECT * FROM response WHERE rep_number=%s', (num,))
        response = main.cur.fetchone()
        if response is not None:
            ignored_roles = ''
            for i in response[4].strip('}{').split(','):
                ignored_roles += f', <@&{i}>'
            await main.help_embed(ctx, f'Response #{num} details:', f'\u2022 Regex: `{response[0]}` \n\u2022 Deletes message? {response[3]} \n\u2022 Ignored roles: \n{ignored_roles[2:]}', response[2], response[1])
        else:
            await main.error_embed(ctx, 'There is no response with that number yet')


def setup(bot):
    bot.add_cog(Response(bot))
