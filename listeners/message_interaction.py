import requests
import json
import logging

import discord
from discord.ext import commands

from utils import PASTE_TOKEN, info_embed, slash_embed

log = logging.getLogger('listeners.message_interaction')


class MessageInteraction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ctx_menu_1 = discord.app_commands.ContextMenu(name='upload to paste.ee', callback=self.paste)
        self.ctx_menu_2 = discord.app_commands.ContextMenu(name='raw contents', callback=self.raw_contents)
        self.ctx_menu_3 = discord.app_commands.ContextMenu(name='embed json', callback=self.embed_json)
        self.ctx_menu_4 = discord.app_commands.ContextMenu(name='member info', callback=self.member_info)
        self.bot.tree.add_command(self.ctx_menu_1)
        self.bot.tree.add_command(self.ctx_menu_2)
        self.bot.tree.add_command(self.ctx_menu_3)
        self.bot.tree.add_command(self.ctx_menu_4)

    async def cog_unload(self):
        self.bot.tree.remove_command(self.ctx_menu_1.name, type=self.ctx_menu_1.type)
        self.bot.tree.remove_command(self.ctx_menu_2.name, type=self.ctx_menu_2.type)
        self.bot.tree.remove_command(self.ctx_menu_3.name, type=self.ctx_menu_3.type)
        self.bot.tree.remove_command(self.ctx_menu_4.name, type=self.ctx_menu_4.type)

    async def paste(self, inter: discord.Interaction, message: discord.Message):
        if not PASTE_TOKEN:
            log.warning('the bot does not have a paste.ee token, so I can\'t upload the message to paste.ee')
            return await slash_embed(
                inter, inter.user, 'The bot does not have a paste token, unable to access paste.ee api.'
            )
        if message.content == '':
            return await slash_embed(inter, inter.user, 'There is no content in this message')
        paste = requests.post(
            url='https://api.paste.ee/v1/pastes',
            json={'sections': [{'name': 'Paste from ' + message.author.name, 'contents': message.content}]},
            headers={'X-Auth-Token': PASTE_TOKEN}
        )
        log.info(f'uploaded contents of message {message.id} to paste.ee with url: {paste.json()["link"]}')
        await slash_embed(
            inter,
            inter.user,
            paste.json()['link'],
            'Contents uploaded to paste.ee',
            self.bot.db.get_embed_color(inter.guild.id)
        )

    async def raw_contents(self, inter: discord.Interaction, message: discord.Message):
        await slash_embed(
            inter, inter.user, f'```{message.content}```', 'Raw contents', self.bot.db.get_embed_color(inter.guild.id)
        )

    async def embed_json(self, inter: discord.Interaction, message: discord.Message):
        if len(message.embeds) < 1:
            return await slash_embed(inter, inter.user, 'There are no embeds on the message you selected', 'No embeds')
        embed_list = '\n'.join(list(json.dumps(embed.to_dict(), indent=4) for embed in message.embeds))
        await slash_embed(
            inter, inter.user, f'```{embed_list}```', 'Embed Json', self.bot.db.get_embed_color(inter.guild.id)
        )

    async def member_info(self, inter: discord.Interaction, message: discord.Message):
        await inter.response.send_message(embed=info_embed(self.bot.db, inter, message.author))


async def setup(bot):
    await bot.add_cog(MessageInteraction(bot))
