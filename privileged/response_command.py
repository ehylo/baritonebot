import re
import mimetypes

import discord
import requests
from discord.ext import commands

from utils.misc import ignored_id_verifier, regex_verifier, role_check
from utils.responses import Responses
from utils.embeds import slash_embed, dm_embed
from utils.const import PASTE_TOKEN


class Trash(discord.ui.Button):
    def __init__(self, bot):
        super().__init__(emoji='🗑️', style=discord.ButtonStyle.gray, custom_id='delete_response')
        self.bot = bot

    async def callback(self, inter: discord.Interaction):
        staff_roles = self.bot.db.admin_ids[inter.guild.id]\
                      + self.bot.db.mod_ids[inter.guild.id]\
                      + self.bot.db.helper_ids[inter.guild.id]
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
        view.add_item(Trash(bot=self.bot))
        self.bot.add_view(view)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.discriminator == '0000':
            return
        if message.author.bot:
            return
        if message.guild is None:
            return
        responses = Responses(self.bot.db, message.guild)
        for index in range(len(responses.titles)):
            if re.search(responses.regexes[index], message.content.lower()) is not None:
                if responses.deletes[index] and not role_check(message.author, responses.ignored_ids[index]):
                    try:
                        await message.delete()
                        dm_channel = await message.author.create_dm()
                        await dm_embed(
                            self.bot.db,
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
                    view.add_item(Trash(bot=self.bot))
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
                                    color=self.bot.db.embed_color[message.guild.id],
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
                        color=self.bot.db.embed_color[message.guild.id],
                        title=responses.titles[index],
                        description=responses.descriptions[index]
                    )
                    embed_var.set_footer(
                        text=f'{message.author.name} | ID: {message.author.id}',
                        icon_url=message.author.display_avatar.url
                    )
                    await message.channel.send(embed=embed_var, view=view)

    @discord.app_commands.command(name='response-new', description='create a new response')
    @discord.app_commands.describe(
        title='the title for the new response (`none` for no title)',
        description='the description for the new response (`none` for no description)',
        regex='the regex this response should try to match with',
        delete='should this response delete the message if the regex matches',
        ignored_ids='roles to be exempt from this response, separate ids with a space (reminder: bypassed and ignored)'
    )
    @discord.app_commands.rename(delete='delete-message', ignored_ids='ignored-ids')
    @discord.app_commands.default_permissions(ban_members=True)
    async def response_new(
        self, inter: discord.Interaction, title: str, description: str, regex: str, delete: bool, ignored_ids: str
    ):
        title = '' if title == 'none' else title
        description = '' if description == 'none' else description
        if not ignored_id_verifier(inter.guild, ignored_ids):
            return await slash_embed(inter, inter.user, 'Could not verify those role ids', 'Bad input')
        if not regex_verifier(regex):
            return await slash_embed(inter, inter.user, 'Could not verify that regex', 'Bad input')
        responses = Responses(self.bot.db, inter.guild)
        responses.new_response(title, description.replace('\\n', '\n'), regex, delete, ignored_ids)
        await slash_embed(
            inter,
            inter.user,
            f'New response created:\n**{title}**',
            'Success!',
            self.bot.db.embed_color[inter.guild.id],
            False
        )

    @discord.app_commands.command(name='response-edit', description='edit a response')
    @discord.app_commands.default_permissions(ban_members=True)
    @discord.app_commands.describe(
        response_num='which response you want to edit',
        title='the title (`none` for no title)',
        description='the description (`none` for no description)',
        regex='the regex this response should try to match with',
        delete='should this response delete the message if the regex matches',
        ignored_ids='roles to be exempt from this response, separate ids with a space (reminder: bypassed and ignored)'
    )
    @discord.app_commands.rename(response_num='response-number', delete='delete-message')
    async def response_edit(
        self,
        inter: discord.Interaction,
        response_num: discord.app_commands.Range[int, 1],
        title: str = None,
        description: str = None,
        regex: str = None,
        delete: bool = None,
        ignored_ids: str = None
    ):
        if ignored_ids is not None and not ignored_id_verifier(inter.guild, ignored_ids):
            return await slash_embed(inter, inter.user, 'Could not verify those role ids', 'Bad input')
        if not regex_verifier(regex):
            return await slash_embed(inter, inter.user, 'Could not verify that regex', 'Bad input')
        responses = Responses(self.bot.db, inter.guild)
        if len(responses.titles) < response_num:
            return await slash_embed(inter, inter.user, 'There are not that many responses', 'Too large')
        if title and description and regex and delete and ignored_ids is None:
            return await slash_embed(inter, inter.user, 'You need to specify an option to edit', 'No options chosen')
        responses.edit_response(response_num - 1, title, description.replace('\\n', '\n'), regex, delete, ignored_ids)
        await slash_embed(
            inter,
            inter.user,
            f'Edited response #{response_num}',
            'Success!',
            self.bot.db.embed_color[inter.guild.id],
            False
        )

    @discord.app_commands.command(name='response-delete', description='delete a response')
    @discord.app_commands.describe(response_num='which response you want to delete')
    @discord.app_commands.rename(response_num='response-number')
    @discord.app_commands.default_permissions(ban_members=True)
    async def response_delete(self, inter: discord.Interaction, response_num: discord.app_commands.Range[int, 1]):
        responses = Responses(self.bot.db, inter.guild)
        if len(responses.titles) < response_num:
            return await slash_embed(inter, inter.user, 'There are not that many responses', 'Too large')
        responses.delete_response(response_num - 1)
        await slash_embed(
            inter,
            inter.user,
            f'Deleted response #{response_num}',
            'Success!',
            self.bot.db.embed_color[inter.guild.id],
            False
        )

    @discord.app_commands.command(name='response-list', description='shows a list of all the current response')
    @discord.app_commands.default_permissions(view_audit_log=True)
    async def response_list(self, inter: discord.Interaction):
        description = ''
        responses = Responses(self.bot.db, inter.guild)
        for response_num in range(len(responses.titles)):
            description += f'**{response_num + 1}.** Title: {responses.titles[response_num]} ' \
                           f'\nRegex: `{responses.regexes[response_num]}`\n'
        await slash_embed(
            inter,
            inter.user,
            description,
            f'Current Responses ({len(responses.titles)}):',
            self.bot.db.embed_color[inter.guild.id]
        )

    @discord.app_commands.command(name='response-details', description='shows details of a specific response')
    @discord.app_commands.describe(response_num='which response you want to get the details of')
    @discord.app_commands.rename(response_num='response-number')
    @discord.app_commands.default_permissions(view_audit_log=True)
    async def response_details(self, inter: discord.Interaction, response_num: discord.app_commands.Range[int, 1]):
        responses = Responses(self.bot.db, inter.guild)
        if len(responses.titles) < response_num:
            return await slash_embed(inter, inter.user, 'There are not that many responses', 'Too large')
        ignored_roles = ''
        for i in responses.ignored_ids[response_num - 1].split(' '):
            ignored_roles += f', <@&{int(i)}>'
        embed_var = discord.Embed(color=self.bot.db.embed_color[inter.guild.id])
        embed_var.title = f'Response #{response_num} details:'
        embed_var.description = f'\u2022 Regex: `{responses.regexes[response_num - 1]}` ' \
                                f'\n\u2022 Deletes message? {responses.deletes[response_num - 1]} ' \
                                f'\n\u2022 Ignored roles: \n{ignored_roles[2:]}'
        title = 'none' if responses.titles[response_num - 1] == '' else responses.titles[response_num - 1]
        description = 'none' if responses.descriptions[response_num-1] == '' else responses.descriptions[response_num-1]
        embed_var.add_field(name=title, value=description)
        embed_var.set_footer(text=f'{inter.user.name} | ID: {inter.user.id}', icon_url=inter.user.display_avatar.url)
        await inter.response.send_message(embed=embed_var, ephemeral=True)


async def setup(bot):
    await bot.add_cog(Response(bot))
