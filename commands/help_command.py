import discord
from discord.ext import commands

from main import bot_db
from utils import const
from utils.embeds import slash_embed


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.discriminator == '0000':
            return
        if message.author.bot:
            return
        if message.guild is None:
            return
        if message.content.startswith('b?'):
            embed_var = discord.Embed(
                color=bot_db.embed_color[message.guild.id],
                title='Removed',
                description='All commands are now slash commands'
            )
            embed_var.set_footer(
                text=f'{message.author.name} | ID: {message.author.id}', icon_url=message.author.display_avatar.url
            )
            return await message.channel.send(embed=embed_var)

    @discord.slash_command(name='help', description='shows commands', guild_ids=[const.GUILD_ID])
    async def setting_searcher(self, ctx):
        return await slash_embed(
            ctx,
            ctx.author,
            '**__Everyone:__**\n'
            'settings, github-issue, github-info, github-pull-request, github-search, help, ignored, releases, ping, '
            'opt-out, user-info, server-info, cringe, cringe-dump, rule'
            '\n**__Helpers:__**\n'
            'cringe-add, mute, unmute, mute-list, response-list, response-details, timeout, un-timeout'
            '\n**__Mods:__**\n'
            'ban, unban, clear, cringe-remove, embed-color, embed, kick, response-new, response-edit, response-delete, '
            'status'
            '\n**__Admins:__**\n'
            'exempt, exempt-list',
            'Slash Commands',
            bot_db.embed_color[ctx.guild.id],
        )


def setup(bot):
    bot.add_cog(Help(bot))
