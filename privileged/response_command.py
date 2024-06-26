import re
import logging

import discord
import requests
from discord.ext import commands

from utils import ignored_id_verifier, regex_verifier, role_check, slash_embed, dm_embed, PASTE_TOKEN

log = logging.getLogger('privileged.response_command')


class Trash(discord.ui.Button):
    def __init__(self, bot):
        super().__init__(emoji='🗑️', style=discord.ButtonStyle.gray, custom_id='delete_response')
        self.bot = bot

    async def callback(self, inter: discord.Interaction):

        # get all the staff roles
        staff_roles = self.bot.db.get_admin_role_ids(inter.guild.id) + self.bot.db.get_mod_role_ids(inter.guild.id)
        staff_roles += self.bot.db.get_helper_role_ids(inter.guild.id)

        for role in inter.user.roles:

            # make sure the person is a staff member, or they were the ones who triggered the embed
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

        # ignore webhooks
        if message.author.discriminator == '0000':
            return
        # ignore messages from bots
        if message.author.bot:
            return
        # ignore dms
        if message.guild is None:
            return

        responses = self.bot.db.get_responses(message.guild.id)

        # go through the responses in the guild the message was sent it
        for response in responses.values():

            # check if it matches the regex
            if re.search(response['regex'], message.content.lower()) is not None:

                has_roles = role_check(message.author, response['ignored_response_ids'])

                # check if the response wants the message to be deleted and the person doesn't have any ignored roles
                if response['delete_message'] and not has_roles:
                    try:
                        await message.delete()
                        dm_channel = await message.author.create_dm()
                        await dm_embed(
                            self.bot.db,
                            message.guild.id,
                            channel=dm_channel,
                            author=message.author,
                            title=response['title'],
                            description=response['description']
                        )
                        log.info(f'{message.author.id} sent a message that matched a deletion response, '
                                 f'regex: {response["regex"]}')
                    except (discord.NotFound, discord.Forbidden, discord.errors.HTTPException):
                        pass

                # check if ! was the start, or the bot was mentioned, or they don't have any ignored roles
                elif not has_roles or self.bot in message.mentions or message.content.startswith('!'):
                    view = discord.ui.View(timeout=None)
                    view.add_item(Trash(bot=self.bot))

                    # if one of these actions was done, the message wants to be deleted
                    if self.bot in message.mentions or message.content.startswith('!'):
                        try:
                            await message.delete()
                        except discord.NotFound:
                            pass

                    # send the response title/description
                    embed_var = discord.Embed(
                        color=self.bot.db.get_embed_color(message.guild.id),
                        title=response['title'],
                        description=response['description']
                    )
                    embed_var.set_footer(
                        text=f'{message.author.name} | ID: {message.author.id}',
                        icon_url=message.author.display_avatar.url
                    )
                    await message.channel.send(embed=embed_var, view=view)
                    log.info(f'{message.author.id} triggered a response with regex: {response["regex"]}')

        # check if the message contains attachments
        if len(message.attachments) > 0:
            for attachment in message.attachments:

                # check if it is a text file
                if 'text' in attachment.content_type:
                    text = await discord.Attachment.read(attachment)

                    # upload it to paste.ee and send embeds
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
                        color=self.bot.db.get_embed_color(message.guild.id),
                        title='Contents uploaded to paste.ee',
                        description=paste_response.json()['link']
                    )
                    embed_var.set_footer(
                        text=f'{message.author.name} | ID: {message.author.id}',
                        icon_url=message.author.display_avatar.url
                    )
                    await message.channel.send(embed=embed_var)
                    log.info(
                        f'{message.author.id} sent an attachment and its contents were uploaded to paste.ee'
                        f' with url: {paste_response.json()["link"]}'
                    )

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

        # switch from None to blank strings
        title = '' if title == 'none' else title
        description = '' if description == 'none' else description

        # verify the given ignored ids
        if not ignored_id_verifier(inter.guild, ignored_ids):
            return await slash_embed(inter, inter.user, 'Could not verify those role ids', 'Bad input')

        # verify the given regex
        if not regex_verifier(regex):
            return await slash_embed(inter, inter.user, 'Could not verify that regex', 'Bad input')

        # add it to the db and send success embeds
        ignored_ids = [int(a) for a in ignored_ids.split(' ')]
        await self.bot.db.new_response(
            inter.guild.id, title, description.replace('\\n', '\n'), regex, delete, ignored_ids
        )
        await slash_embed(
            inter,
            inter.user,
            f'New response created:\n**{title}**',
            'Success!',
            self.bot.db.get_embed_color(inter.guild.id),
            False
        )
        log.info(f'{inter.user.id} created a new response in {inter.guild.id}')

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

        # verify the given ignored ids
        if ignored_ids is not None and not ignored_id_verifier(inter.guild, ignored_ids):
            return await slash_embed(inter, inter.user, 'Could not verify those role ids', 'Bad input')

        # verify the given regex
        if not regex_verifier(regex):
            return await slash_embed(inter, inter.user, 'Could not verify that regex', 'Bad input')

        responses = self.bot.db.get_responses(inter.guild.id)

        # make sure the response number is correct
        if len(responses) < response_num:
            return await slash_embed(inter, inter.user, 'There are not that many responses', 'Too large')

        # make sure a required attribute is given
        if title and description and regex and delete and ignored_ids is None:
            return await slash_embed(inter, inter.user, 'You need to specify an option to edit', 'No options chosen')

        # make sure the newlines actually show
        if description is not None:
            description = description.replace('\\n', '\n')

        await self.bot.db.edit_response(
            inter.guild.id, list(responses.keys())[response_num - 1], title, description, regex, delete
        )
        await slash_embed(
            inter,
            inter.user,
            f'Edited response #{response_num}',
            'Success!',
            self.bot.db.get_embed_color(inter.guild.id),
            False
        )
        log.info(f'{inter.user.id} edited a response in {inter.guild.id}')

    @discord.app_commands.command(name='response-delete', description='delete a response')
    @discord.app_commands.describe(response_num='which response you want to delete')
    @discord.app_commands.rename(response_num='response-number')
    @discord.app_commands.default_permissions(ban_members=True)
    async def response_delete(self, inter: discord.Interaction, response_num: discord.app_commands.Range[int, 1]):
        responses = self.bot.db.get_responses(inter.guild.id)

        # make sure the response number is correct
        if len(responses) < response_num:
            return await slash_embed(inter, inter.user, 'There are not that many responses', 'Too large')

        await self.bot.db.delete_response(inter.guild.id, list(responses.keys())[response_num - 1])
        await slash_embed(
            inter,
            inter.user,
            f'Deleted response #{response_num}',
            'Success!',
            self.bot.db.get_embed_color(inter.guild.id),
            False
        )
        log.info(f'{inter.user.id} deleted a response in {inter.guild.id}')

    @discord.app_commands.command(name='response-list', description='shows a list of all the current response')
    @discord.app_commands.default_permissions(view_audit_log=True)
    async def response_list(self, inter: discord.Interaction):
        description = ''
        responses = self.bot.db.get_responses(inter.guild.id)

        # go through each response and grab meaningful information from it
        for i, response_num in enumerate(responses):
            description += f'**{i + 1}.** Title: {responses[response_num]["title"]} ' \
                           f'\nRegex: `{responses[response_num]["regex"]}`\n'

        await slash_embed(
            inter,
            inter.user,
            description,
            f'Current Responses ({len(responses)}):',
            self.bot.db.get_embed_color(inter.guild.id)
        )

    @discord.app_commands.command(name='response-details', description='shows details of a specific response')
    @discord.app_commands.describe(response_num='which response you want to get the details of')
    @discord.app_commands.rename(response_num='response-number')
    @discord.app_commands.default_permissions(view_audit_log=True)
    async def response_details(self, inter: discord.Interaction, response_num: discord.app_commands.Range[int, 1]):
        responses = self.bot.db.get_responses(inter.guild.id)

        # make sure the response number is correct
        if len(responses) < response_num:
            return await slash_embed(inter, inter.user, 'There are not that many responses', 'Too large')

        resp_dict = list(responses.items())[response_num - 1][1]

        # make a string list of ignored roles
        ignored_roles = ''
        for i in resp_dict['ignored_response_ids']:
            ignored_roles += f', <@&{i}>'

        # start building the embed
        embed_var = discord.Embed(color=self.bot.db.get_embed_color(inter.guild.id))
        embed_var.title = f'Response #{response_num} details:'
        embed_var.description = f'\u2022 Regex: `{resp_dict["regex"]}` ' \
                                f'\n\u2022 Deletes message? {resp_dict["delete_message"]} ' \
                                f'\n\u2022 Ignored roles: \n{ignored_roles[2:]}'

        # make sure our embed length is within discord's bounds
        if len(embed_var.description) > 4095:
            embed_var.description = embed_var.description[:4090] + '...'

        # make sure we check for title/description being None
        title = 'none' if resp_dict['title'] == '' else resp_dict['title']
        description = 'none' if resp_dict['description'] == '' else resp_dict['description']

        # check to make sure title is in bounds
        if len(title) > 255:
            title = title[:250] + '...'

        # make sure description is in bounds
        if len(description) > 1023:
            description = description[:1018] + '...'

        # finish off embed and send
        embed_var.add_field(name=title, value=description)
        embed_var.set_footer(text=f'{inter.user.name} | ID: {inter.user.id}', icon_url=inter.user.display_avatar.url)
        await inter.response.send_message(embed=embed_var, ephemeral=True)


async def setup(bot):
    await bot.add_cog(Response(bot))
