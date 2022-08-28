import re
import mimetypes

import discord
import requests
from discord.ext import commands
from discord.commands import Option

from main import bot_db
from utils.misc import ignored_id_verifier, regex_verifier, role_check
from utils.responses import Responses
from utils.embeds import slash_embed, dm_embed
from utils.const import GUILD_ID, PASTE_TOKEN


class Trash(discord.ui.Button):
    def __init__(self):
        super().__init__(emoji='🗑️', style=discord.ButtonStyle.gray, custom_id='delete_response')

    async def callback(self, inter):
        staff_roles = bot_db.admin_ids[inter.guild.id]+bot_db.mod_ids[inter.guild.id]+bot_db.helper_ids[inter.guild.id]
        for role in inter.user.roles:
            if role.id in staff_roles or inter.user.id == int(inter.message.embeds[0].footer.text.split('ID: ')[1]):
                return await inter.message.delete()
        return await slash_embed(inter, inter.user, 'You did not trigger this response!', 'Unable to delete')


class Response(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        view = discord.ui.View(timeout=None)
        view.add_item(Trash())
        self.bot.add_view(view)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.discriminator == '0000':
            return
        if message.author.bot:
            return
        if message.guild is None:
            return
        responses = Responses(bot_db, message.guild)
        for index in range(len(responses.titles)):
            if re.search(responses.regexes[index], message.content.lower()) is not None:
                if responses.deletes[index] and not role_check(message.author, responses.ignored_ids[index]):
                    try:
                        await message.delete()
                        dm_channel = await message.author.create_dm()
                        await dm_embed(
                            bot_db,
                            message.guild.id,
                            channel=dm_channel,
                            author=message.author,
                            title=responses.titles[index],
                            description=responses.descriptions[index]
                        )
                    except (discord.NotFound, discord.Forbidden, discord.errors.HTTPException):
                        pass
                elif not role_check(message.author, responses.ignored_ids[index]) or \
                        self.bot in message.mentions or message.content.startswith('!'):
                    view = discord.ui.View(timeout=None)
                    view.add_item(Trash())
                    if len(message.attachments) > 0:
                        for attachment in message.attachments:
                            file_type = mimetypes.guess_type(attachment.url)
                            if file_type[0] is not None:
                                file_type = file_type[0].split('/')[0]
                            if attachment.url.lower().endswith(
                                (
                                    '.log', '.json5', '.json', '.py', '.sh', '.config', '.toml', '.bat', '.cfg'
                                )
                            ) or file_type == 'text':
                                text = await discord.Attachment.read(attachment)
                                paste_response = requests.post(
                                    url='https://api.paste.ee/v1/pastes',
                                    json={
                                        'sections': [
                                            {
                                                'name': 'Paste from ' + str(message.author),
                                                'contents': ('\n'.join((text.decode('UTF-8')).splitlines()))
                                            }
                                        ]
                                    },
                                    headers={'X-Auth-Token': PASTE_TOKEN}
                                )
                                embed_var = discord.Embed(
                                    color=bot_db.embed_color[message.guild.id],
                                    title='Contents uploaded to paste.ee',
                                    description=paste_response.json()['link']
                                )
                                embed_var.set_footer(
                                    text=f'{message.author.name} | ID: {message.author.id}',
                                    icon_url=message.author.display_avatar.url
                                )
                                await message.channel.send(embed=embed_var)
                    if self.bot in message.mentions or message.content.startswith('!'):
                        try:
                            await message.delete()
                        except discord.NotFound:
                            pass
                    embed_var = discord.Embed(
                        color=bot_db.embed_color[message.guild.id],
                        title=responses.titles[index],
                        description=responses.descriptions[index]
                    )
                    embed_var.set_footer(
                        text=f'{message.author.name} | ID: {message.author.id}', icon_url=message.author.display_avatar.url
                    )
                    await message.channel.send(embed=embed_var, view=view)

    @discord.slash_command(
        name='response-new', description='create a new response', guild_ids=[GUILD_ID]
    )
    @discord.default_permissions(ban_members=True)
    async def response_new(
        self,
        ctx,
        title: Option(name='title', description='the title for the new response (`none` for no title)', required=True),
        description: Option(
            name='description',
            description='the description for the new response (`none` for no description)',
            required=True
        ),
        regex: Option(name='regex', description='the regex this response should try to match with', required=True),
        delete: Option(
            bool,
            name='delete-message',
            description='should this response delete the message if the regex matches',
            required=True
        ),
        ignored_ids: Option(
            name='ignored-ids',
            description='roles to be exempt from this response, '
                        'separate ids with a space (reminder: bypassed and ignored)',
            required=True
        )
    ):
        title = '' if title == 'none' else title
        description = '' if description == 'none' else description
        if not ignored_id_verifier(ctx.guild, ignored_ids):
            return await slash_embed(ctx, ctx.author, 'Could not verify those role ids', 'Bad input')
        if not regex_verifier(regex):
            return await slash_embed(ctx, ctx.author, 'Could not verify that regex', 'Bad input')
        responses = Responses(bot_db, ctx.guild)
        responses.new_response(title, description, regex, delete, ignored_ids)
        await slash_embed(
            ctx,
            ctx.author,
            f'New response created:\n**{title}**',
            'Success!',
            bot_db.embed_color[ctx.guild.id],
            False
        )

    @discord.slash_command(
        name='response-edit', description='edit a response', guild_ids=[GUILD_ID]
    )
    @discord.default_permissions(ban_members=True)
    async def response_edit(
        self,
        ctx,
        response_num: Option(
            int,
            name='response-number',
            description='which response you want to edit',
            min_value=1,
            required=True
        ),
        title: Option(name='title', description='the title (`none` for no title)', required=False),
        description: Option(
            name='description', description='the description (`none` for no description)', required=False
        ),
        regex: Option(name='regex', description='the regex this response should try to match with', required=False),
        delete: Option(
            bool,
            name='delete-message',
            description='should this response delete the message if the regex matches',
            required=False
        ),
        ignored_ids: Option(
            name='ignored-ids',
            description='roles to be exempt from this response, '
                        'separate ids with a space (reminder: bypassed and ignored)',
            required=False
        )
    ):
        if ignored_ids is not None and not ignored_id_verifier(ctx.guild, ignored_ids):
            return await slash_embed(ctx, ctx.author, 'Could not verify those role ids', 'Bad input')
        if regex is not None and not regex_verifier(regex):
            return await slash_embed(ctx, ctx.author, 'Could not verify that regex', 'Bad input')
        responses = Responses(bot_db, ctx.guild)
        if len(responses.titles) < response_num:
            return await slash_embed(ctx, ctx.author, 'There are not that many responses', 'Too large')
        if title and description and regex and delete and ignored_ids is None:
            return await slash_embed(ctx, ctx.author, 'You need to specify an option to edit', 'No options chosen')
        responses.edit_response(response_num - 1, title, description, regex, delete, ignored_ids)
        await slash_embed(
            ctx,
            ctx.author,
            f'Edited response #{response_num}',
            'Success!',
            bot_db.embed_color[ctx.guild.id],
            False
        )

    @discord.slash_command(name='response-delete', description='delete a response', guild_ids=[GUILD_ID])
    @discord.default_permissions(ban_members=True)
    async def response_delete(
        self,
        ctx,
        response_num: Option(
            int,
            name='response-number',
            description='which response you want to delete',
            min_value=1,
            required=True
        )
    ):
        responses = Responses(bot_db, ctx.guild)
        if len(responses.titles) < response_num:
            return await slash_embed(ctx, ctx.author, 'There are not that many responses', 'Too large')
        responses.delete_response(response_num - 1)
        await slash_embed(
            ctx, ctx.author, f'Deleted response #{response_num}', 'Success!', bot_db.embed_color[ctx.guild.id], False
        )

    @discord.slash_command(
        name='response-list',
        description='shows a list of all the current response',
        guild_ids=[GUILD_ID]
    )
    @discord.default_permissions(view_audit_log=True)
    async def response_list(self, ctx):
        description = ''
        responses = Responses(bot_db, ctx.guild)
        for response_num in range(len(responses.titles)):
            description += f'**{response_num + 1}.** Title: {responses.titles[response_num]} ' \
                           f'\nRegex: `{responses.regexes[response_num]}`\n'
        await slash_embed(
            ctx,
            ctx.author,
            description,
            f'Current Responses ({len(responses.titles)}):',
            bot_db.embed_color[ctx.guild.id]
        )

    @discord.slash_command(
        name='response-details',
        description='shows details of a specific response',
        guild_ids=[GUILD_ID]
    )
    @discord.default_permissions(view_audit_log=True)
    async def response_details(
        self,
        ctx,
        response_num: Option(
            int,
            name='response-number',
            description='which response you want to get the details of',
            min_value=1,
            required=True
        )
    ):
        responses = Responses(bot_db, ctx.guild)
        if len(responses.titles) < response_num:
            return await slash_embed(ctx, ctx.author, 'There are not that many responses', 'Too large')
        ignored_roles = ''
        for i in responses.ignored_ids[response_num - 1].split(' '):
            ignored_roles += f', <@&{int(i)}>'
        embed_var = discord.Embed(color=bot_db.embed_color[ctx.guild.id])
        embed_var.title = f'Response #{response_num} details:'
        embed_var.description = f'\u2022 Regex: `{responses.regexes[response_num - 1]}` ' \
                                f'\n\u2022 Deletes message? {responses.deletes[response_num - 1]} ' \
                                f'\n\u2022 Ignored roles: \n{ignored_roles[2:]}'
        title = 'none' if responses.titles[response_num - 1] == '' else responses.titles[response_num - 1]
        description = 'none' if responses.descriptions[response_num-1] == '' else responses.descriptions[response_num-1]
        embed_var.add_field(name=title, value=description)
        embed_var.set_footer(text=f'{ctx.author.name} | ID: {ctx.author.id}', icon_url=ctx.author.display_avatar.url)
        await ctx.respond(embed=embed_var, ephemeral=True)


def setup(bot):
    bot.add_cog(Response(bot))
