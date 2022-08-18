import requests
import json

import discord
from discord.ext import commands

from main import bot_db
from utils.const import GUILD_ID, PASTE_TOKEN
from utils.misc import info_embed
from utils.embeds import slash_embed


class MessageInteraction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.message_command(name='upload to paste.ee', guild_ids=[GUILD_ID])
    async def paste(self, ctx, message):
        paste = requests.post(
            url='https://api.paste.ee/v1/pastes',
            json={'sections': [{'name': 'Paste from ' + message.author.name, 'contents': message.content}]},
            headers={'X-Auth-Token': PASTE_TOKEN}
        )
        await slash_embed(
            ctx, ctx.author, paste.json()['link'], 'Contents uploaded to paste.ee', bot_db.embed_color[ctx.guild.id]
        )

    @discord.message_command(name='raw contents', guild_ids=[GUILD_ID])
    async def raw_contents(self, ctx, message):
        await slash_embed(
            ctx, ctx.author, f'```{message.content}```', 'Raw contents', bot_db.embed_color[ctx.guild.id]
        )

    @discord.message_command(name='embed json', guild_ids=[GUILD_ID])
    async def embed_json(self, ctx, message):
        if len(message.embeds) < 1:
            return await slash_embed(ctx, ctx.author, 'There are no embeds on the message you selected', 'No embeds')
        embed_list = '\n'.join(list(json.dumps(embed.to_dict(), indent=4) for embed in message.embeds))
        await slash_embed(ctx, ctx.author, f'```{embed_list}```', 'Embed Json', bot_db.embed_color[ctx.guild.id])

    @discord.message_command(name='member-info', guild_ids=[GUILD_ID])
    async def member_info(self, ctx, _message):
        await ctx.respond(embed=info_embed(bot_db, ctx, ctx.author))


def setup(bot):
    bot.add_cog(MessageInteraction(bot))
