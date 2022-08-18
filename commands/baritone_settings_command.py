import discord
from discord.ext import commands
from discord.commands import Option

import main
from main import bot_db
from utils import const
from utils.embeds import slash_embed


class BackwardButton(discord.ui.Button):
    def __init__(self):
        super().__init__(emoji='◀️', style=discord.ButtonStyle.blurple, custom_id='settings_back', disabled=True)

    async def callback(self, inter):
        if self.view.old_message:
            return await slash_embed(
                inter,
                inter.user,
                'This message was sent before my current session so I cannot cycle between the pages',
                'Search again',
                interaction_response=True
            )
        self.view.current_page -= 1
        self.view.children[1].disabled = False
        pages = main.version_matcher[self.view.version].search(self.view.term)
        if self.view.current_page == 0:
            self.disabled = True
        await slash_embed(
            ctx=inter,
            author=inter.user,
            description=pages[self.view.current_page],
            color=bot_db.embed_color[inter.guild.id],
            ephemeral=False,
            view=self.view,
            interaction=True
        )


class ForwardButton(discord.ui.Button):
    def __init__(self):
        super().__init__(emoji='▶️', style=discord.ButtonStyle.blurple, custom_id='settings_forward')

    async def callback(self, inter):
        if self.view.old_message:
            return await slash_embed(
                inter,
                inter.user,
                'This message was sent before my current session so I cannot cycle between the pages',
                'Search again',
                interaction_response=True
            )
        self.view.current_page += 1
        self.view.children[0].disabled = False
        pages = main.version_matcher[self.view.version].search(self.view.term)
        if self.view.current_page == len(pages) - 1:
            self.disabled = True
        return await slash_embed(
            ctx=inter,
            author=inter.user,
            description=pages[self.view.current_page],
            color=bot_db.embed_color[inter.guild.id],
            ephemeral=False,
            view=self.view,
            interaction=True
        )


class BaritoneSettings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        view = discord.ui.View(timeout=None)
        view.old_message = True
        view.add_item(BackwardButton())
        view.add_item(ForwardButton())
        self.bot.add_view(view)

    @discord.slash_command(name='settings', description='finds baritone settings', guild_ids=[const.GUILD_ID])
    async def setting_searcher(
        self,
        ctx,
        version: Option(
            name='version',
            description='the baritone version you want to find settings for',
            choices=['1.2.15', '1.8.3', '1.9'],
            required=True
        ),
        term: Option(name='term', description='The term you want to search for', required=True)
    ):
        content = main.version_matcher[version].search(term)
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
        view.term = term
        view.version = version
        view.old_message = False
        view.current_page = 0
        view.add_item(BackwardButton())
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
