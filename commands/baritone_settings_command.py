# TODO fix back and forward button code and test

import discord
from discord.ext import commands
from discord.commands import Option


from main import baritone_settings, bot_db
from utils import const
from utils.embeds import slash_embed


class BackwardButton(discord.ui.Button):
    def __init__(self):
        super().__init__(emoji='◄', style=discord.ButtonStyle.blurple, custom_id='settings_back')

    async def callback(self, inter):
        data = inter.message.interaction.data['data']['options']
        version = data[0]['value']
        term = data[1]['value']
        old_page = 2
        total_pages = len(baritone_settings.search(term, version))
        if old_page - 1 == 1:
            self.disabled = True
        await slash_embed(
            ctx=inter,
            author=inter.user,
            description=baritone_settings.search(term, version)[old_page - 2],
            title=f'{old_page - 1}/{total_pages}',
            color=bot_db.embed_color[inter.guild.id],
            ephemeral=False,
            view=self.view,
            interaction=True
        )


class CurrentPage(discord.ui.Button):
    def __init__(self, total_pages):
        super().__init__(label='1/' + total_pages, style=discord.ButtonStyle.green, custom_id='current_page')

    async def button_callback(self, button, inter):
        # don't do anything, this is just visual
        pass


class ForwardButton(discord.ui.Button):
    def __init__(self):
        super().__init__(emoji='►', style=discord.ButtonStyle.blurple, custom_id='settings_forward')

    async def button_callback(self, button, inter):
        data = inter.message.interaction.data['data']['options']
        version = data[0]['value']
        term = data[1]['value']
        old_page = 1
        total_pages = len(baritone_settings.search(term, version))
        if old_page + 1 == total_pages:
            button.disabled = True
        await slash_embed(
            ctx=inter,
            author=inter.user,
            description=baritone_settings.search(term, version)[old_page],
            title=f'{old_page + 1}/{total_pages}',
            color=bot_db.embed_color[inter.guild.id],
            ephemeral=False,
            view=self.view,
            interaction=True
        )


class BaritoneSettings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name='settings', description='finds baritone settings', guild_ids=[const.GUILD_ID])
    async def setting_searcher(
        self,
        ctx,
        version: Option(
            str,
            name='baritone version',
            description='the baritone version you want to find settings for',
            choices=['1.2.15', '1.6.3', '1.7.2', '1.8.2'],
            default='1.2.15',
            required=True
        ),
        term: Option(str, name='search term', description='The term you want to search for', required=True)
    ):
        content = baritone_settings.search(term, version)
        if content == ['']:
            return await slash_embed(
                ctx,
                ctx.author,
                'No settings were found with that search :(',
                color=bot_db.embed_color[ctx.guild.id],
                ephemeral=False,
            )
        if len(content) == 1:
            return await slash_embed(
                ctx,
                ctx.author,
                content[0],
                color=bot_db.embed_color[ctx.guild.id],
                ephemeral=False
            )
        view = discord.ui.View(timeout=None)
        view.add_item(BackwardButton())
        view.add_item(CurrentPage(len(content)))
        view.add_item(ForwardButton())
        return await slash_embed(
            ctx,
            ctx.author,
            content[0],
            color=bot_db.embed_color[ctx.guild.id],
            ephemeral=False,
            view=view
        )


def setup(bot):
    bot.add_cog(BaritoneSettings(bot))
