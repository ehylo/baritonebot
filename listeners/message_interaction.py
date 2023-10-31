import requests
import json

import discord
from discord.ext import commands

from utils.const import PASTE_TOKEN
from utils.misc import info_embed
from utils.embeds import slash_embed


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
            # TODO: Log that the paste could not be made due to no token
            return await slash_embed(
                inter, inter.user, 'The bot does not have a paste token, unable to access paste.ee api.'
            )
        paste = requests.post(
            url='https://api.paste.ee/v1/pastes',
            json={'sections': [{'name': 'Paste from ' + message.author.name, 'contents': message.content}]},
            headers={'X-Auth-Token': PASTE_TOKEN}
        )
        await slash_embed(
            inter,
            inter.user,
            paste.json()['link'],
            'Contents uploaded to paste.ee',
            self.bot.db.embed_color[inter.guild.id]
        )

    async def raw_contents(self, inter: discord.Interaction, message: discord.Message):
        await slash_embed(
            inter, inter.user, f'```{message.content}```', 'Raw contents', self.bot.db.embed_color[inter.guild.id]
        )

    async def embed_json(self, inter: discord.Interaction, message: discord.Message):
        if len(message.embeds) < 1:
            return await slash_embed(inter, inter.user, 'There are no embeds on the message you selected', 'No embeds')
        embed_list = '\n'.join(list(json.dumps(embed.to_dict(), indent=4) for embed in message.embeds))
        await slash_embed(
            inter, inter.user, f'```{embed_list}```', 'Embed Json', self.bot.db.embed_color[inter.guild.id]
        )

    async def member_info(self, inter: discord.Interaction, _message: discord.Message):
        await inter.response.send_message(embed=info_embed(self.bot.db, inter, inter.user))


async def setup(bot):
    await bot.add_cog(MessageInteraction(bot))
