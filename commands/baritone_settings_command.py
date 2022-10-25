import discord
from discord.ext import commands

from utils.embeds import slash_embed
from utils import const


class BackwardButton(discord.ui.Button):
    def __init__(self, bot):
        super().__init__(emoji='◀️', style=discord.ButtonStyle.blurple, custom_id='settings_back', disabled=True)
        self.bot = bot

    async def callback(self, inter: discord.Interaction):
        if self.view.old_message:
            return await slash_embed(
                inter,
                inter.user,
                'This message was sent before my current session so I cannot cycle between the pages',
                'Search again'
            )
        self.view.current_page -= 1
        self.view.children[1].disabled = False
        pages = self.view.version.search(self.view.term)
        if self.view.current_page == 0:
            self.disabled = True
        await slash_embed(
            inter,
            author=inter.user,
            description=pages[self.view.current_page],
            color=self.bot.db.embed_color[inter.guild.id],
            ephemeral=False,
            view=self.view,
            is_interaction=True
        )


class ForwardButton(discord.ui.Button):
    def __init__(self, bot):
        super().__init__(emoji='▶️', style=discord.ButtonStyle.blurple, custom_id='settings_forward')
        self.bot = bot

    async def callback(self, inter: discord.Interaction):
        if self.view.old_message:
            return await slash_embed(
                inter,
                inter.user,
                'This message was sent before my current session so I cannot cycle between the pages',
                'Search again',
            )
        self.view.current_page += 1
        self.view.children[0].disabled = False
        pages = self.view.version.search(self.view.term)
        if self.view.current_page == len(pages) - 1:
            self.disabled = True
        return await slash_embed(
            inter,
            author=inter.user,
            description=pages[self.view.current_page],
            color=self.bot.db.embed_color[inter.guild.id],
            ephemeral=False,
            view=self.view,
            is_interaction=True
        )


class BaritoneSettings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        view = discord.ui.View(timeout=None)
        view.old_message = True
        view.add_item(BackwardButton(bot=self.bot))
        view.add_item(ForwardButton(bot=self.bot))
        self.bot.add_view(view)

    @discord.app_commands.command(name='settings', description='finds baritone settings')
    @discord.app_commands.describe(
        version='the baritone version you want to find settings for',
        term='The term you want to search for'
    )
    async def setting_searcher(self, inter: discord.Interaction, version: const.baritone_settings_versions, term: str):
        content = version.value.search(term)
        if content == ['']:
            return await slash_embed(
                inter,
                inter.user,
                'No settings were found with that search :(',
                color=self.bot.db.embed_color[inter.guild.id],
                ephemeral=False,
            )
        if len(content) == 1:
            return await slash_embed(
                inter,
                inter.user,
                content[0],
                color=self.bot.db.embed_color[inter.guild.id],
                ephemeral=False
            )
        view = discord.ui.View(timeout=None)
        view.term = term
        view.version = version.value
        view.old_message = False
        view.current_page = 0
        view.add_item(BackwardButton(bot=self.bot))
        view.add_item(ForwardButton(bot=self.bot))
        return await slash_embed(
            inter,
            inter.user,
            content[0],
            color=self.bot.db.embed_color[inter.guild.id],
            ephemeral=False,
            view=view
        )


async def setup(bot):
    await bot.add_cog(BaritoneSettings(bot))
