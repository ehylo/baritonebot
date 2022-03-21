import discord
from discord.ext import commands
from discord.commands import Option

from main import bot_db
from utils.const import GUILD_ID
from utils.embeds import slash_embed


class UndoAddIgnored(discord.ui.View):
    @discord.ui.button(label='Undo', emoji='↪', style=discord.ButtonStyle.grey, custom_id='add_ignore')
    async def button_callback(self, button, inter):
        button.disabled = True
        if inter.guild.get_role(bot_db.ignore_id[inter.guild.id]) not in inter.user.roles:
            return await slash_embed(inter, inter.user, 'You don\'t have the ignored role', view=self, interaction=True)
        await inter.user.remove_roles(inter.guild.get_role(bot_db.ignore_id[inter.guild.id]))
        await slash_embed(
            inter,
            inter.user,
            'Your messages will now trigger the response regexes.',
            'Ignored role removed',
            bot_db.embed_color[inter.guild.id],
            view=self,
            interaction=True
        )


class UndoRemoveIgnored(discord.ui.View):
    @discord.ui.button(label='Undo', emoji='↪', style=discord.ButtonStyle.grey, custom_id='remove_ignore')
    async def button_callback(self, button, inter):
        button.disabled = True
        if inter.guild.get_role(bot_db.ignore_id[inter.guild.id]) in inter.user.roles:
            return await slash_embed(inter, inter.user, 'You have the ignored role', view=self, interaction=True)
        await inter.user.add_roles(inter.guild.get_role(bot_db.ignore_id[inter.guild.id]))
        await slash_embed(
            inter,
            inter.user,
            'Your messages will now not trigger the response regexes unless you ping me.',
            'Ignored role added',
            bot_db.embed_color[inter.guild.id],
            view=self,
            interaction=True
        )


class Ignored(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(
        name='ignored',
        description='Add/remove the ignored role, if you have this you will not trigger most of the responses',
        guild_ids=[GUILD_ID],
    )
    async def ignored(
        self,
        ctx,
        action: Option(
            str,
            name='action',
            description='Add or remove the ignored role',
            choices=['Add', 'Remove'],
            required=True
        )
    ):
        if action == 'Add':
            if ctx.guild.get_role(bot_db.ignore_id[ctx.guild.id]) in ctx.author.roles:
                return await slash_embed(ctx, ctx.author, 'You already have the ignored role.')
            await ctx.author.add_roles(ctx.guild.get_role(bot_db.ignore_id[ctx.guild.id]))
            await slash_embed(
                ctx,
                ctx.author,
                'Your messages will now not trigger the response regexes unless you ping me.',
                'Ignored role added',
                bot_db.embed_color[ctx.guild.id],
                view=UndoAddIgnored(timeout=None)
            )
        if action == 'Remove':
            if ctx.guild.get_role(bot_db.ignore_id[ctx.guild.id]) not in ctx.author.roles:
                return await slash_embed(ctx, ctx.author, 'You don\'t have the ignored role.')
            await ctx.author.remove_roles(ctx.guild.get_role(bot_db.ignore_id[ctx.guild.id]))
            await slash_embed(
                ctx,
                author=ctx.author,
                title='Ignored role removed',
                description='Your messages will now trigger the response regexes.',
                color=bot_db.embed_color[ctx.guild.id],
                view=UndoRemoveIgnored(timeout=None)
            )

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(UndoAddIgnored(timeout=None))
        self.bot.add_view(UndoRemoveIgnored(timeout=None))


def setup(bot):
    bot.add_cog(Ignored(bot))
