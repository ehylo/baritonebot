import discord
from discord.ext import commands

from utils import slash_embed


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.discriminator == '0000':
            return
        if message.author.bot:
            return
        if message.guild is None:
            return
        if message.content.startswith('b?'):
            embed_var = discord.Embed(
                color=self.bot.db.get_embed_color(message.guild.id),
                title='Removed',
                description='All commands are now slash commands'
            )
            embed_var.set_footer(
                text=f'{message.author.name} | ID: {message.author.id}', icon_url=message.author.display_avatar.url
            )
            return await message.channel.send(embed=embed_var)

    @discord.app_commands.command(description='shows commands')
    async def help(self, inter: discord.Interaction):
        return await slash_embed(
            inter,
            inter.user,
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
            self.bot.db.get_embed_color(inter.guild.id),
        )


async def setup(bot):
    await bot.add_cog(Help(bot))
