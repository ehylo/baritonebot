import discord
from discord.ext import commands
from discord.commands import Option

from main import bot_db
from utils.const import GUILD_ID
from utils.embeds import slash_embed


class UndoAddReleases(discord.ui.View):
    @discord.ui.button(label='Undo', emoji='↪', style=discord.ButtonStyle.grey, custom_id='add_release')
    async def button_callback(self, button, inter):
        button.disabled = True
        if inter.guild.get_role(bot_db.release_id[inter.guild.id]) not in inter.user.roles:
            return await slash_embed(inter, inter.user, 'You don\'t have the release role', view=self, interaction=True)
        await inter.user.remove_roles(inter.guild.get_role(bot_db.release_id[inter.guild.id]))
        await slash_embed(
            inter,
            inter.user,
            'You will not be pinged when a new release is made now.',
            'Releases role removed',
            bot_db.embed_color[inter.guild.id],
            view=self,
            interaction=True
        )


class UndoRemoveReleases(discord.ui.View):
    @discord.ui.button(label='Undo', emoji='↪', style=discord.ButtonStyle.grey, custom_id='remove_release')
    async def button_callback(self, button, inter):
        button.disabled = True
        if inter.guild.get_role(bot_db.release_id[inter.guild.id]) in inter.user.roles:
            return await slash_embed(inter, inter.user, 'You have the release role', view=self, interaction=True)
        await inter.user.add_roles(inter.guild.get_role(bot_db.release_id[inter.guild.id]))
        await slash_embed(
            inter,
            inter.user,
            'You will now be pinged when a new release is made!',
            'Releases role added',
            bot_db.embed_color[inter.guild.id],
            view=self,
            interaction=True
        )


class Releases(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(
        name='releases',
        description='Add/remove the releases role, if you have this you will be pinged when a new release comes out',
        guild_ids=[GUILD_ID],
    )
    async def releases(
        self,
        ctx,
        action: Option(
            str,
            name='action',
            description='Add or remove the releases role',
            choices=['Add', 'Remove'],
            required=True
        )
    ):
        if action == 'Add':
            if ctx.guild.get_role(bot_db.release_id[ctx.guild.id]) in ctx.author.roles:
                return await slash_embed(ctx, ctx.author, 'You already have the releases role.')
            await ctx.author.add_roles(ctx.guild.get_role(bot_db.release_id[ctx.guild.id]))
            await slash_embed(
                ctx,
                ctx.author,
                'You will now be pinged when a new release is made!',
                'Releases role added',
                bot_db.embed_color[ctx.guild.id],
                view=UndoAddReleases(timeout=None)
            )
        if action == 'Remove':
            if ctx.guild.get_role(bot_db.release_id[ctx.guild.id]) not in ctx.author.roles:
                return await slash_embed(ctx, ctx.author, 'You don\'t have the releases role.')
            await ctx.author.remove_roles(ctx.guild.get_role(bot_db.release_id[ctx.guild.id]))
            await slash_embed(
                ctx,
                author=ctx.author,
                title='Releases role removed',
                description='You will not be pinged when a new release is made now.',
                color=bot_db.embed_color[ctx.guild.id],
                view=UndoRemoveReleases(timeout=None)
            )

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(UndoAddReleases(timeout=None))
        self.bot.add_view(UndoRemoveReleases(timeout=None))


def setup(bot):
    bot.add_cog(Releases(bot))
