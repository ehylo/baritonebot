import discord
from discord.ext import commands
from discord.commands import Option

from utils.const import GUILD_ID
from utils.embeds import slash_embed
from utils.misc import get_channel
from main import bot_db


class UndoAddExempt(discord.ui.View):
    def __init__(self, bot):
        self.bot = bot
        super().__init__(timeout=None)

    @discord.ui.button(label='Undo', emoji='↪', style=discord.ButtonStyle.grey, custom_id='add_exempt')
    async def button_callback(self, button, inter):
        button.disabled = True
        exempt_list = bot_db.exempted_ids[inter.guild.id]
        channel = await get_channel(
            self.bot,
            int(inter.message.embeds[0].description.split(' will')[0].split('in ')[1][2:-1])
        )
        if channel.id not in bot_db.exempted_ids[inter.guild.id]:
            return await slash_embed(inter, inter.user, 'That channel isn\'t exempted', view=self, interaction=True)
        exempt_list.remove(channel.id)
        bot_db.update_exempted_ids(inter.guild.id, exempt_list)
        await slash_embed(
            inter,
            inter.user,
            f'Edited/deleted messages in {channel.mention} will now be logged',
            'Channel un-exempted',
            bot_db.embed_color[inter.guild.id],
            view=self,
            interaction=True
        )


class UndoRemoveExempt(discord.ui.View):
    def __init__(self, bot):
        self.bot = bot
        super().__init__(timeout=None)

    @discord.ui.button(label='Undo', emoji='↪', style=discord.ButtonStyle.grey, custom_id='remove_exempt')
    async def button_callback(self, button, inter):
        button.disabled = True
        channel = await get_channel(
            self.bot,
            int(inter.message.embeds[0].description.split(' will')[0].split('in ')[1][2:-1])
        )
        if channel.id in bot_db.exempted_ids[inter.guild.id]:
            return await slash_embed(inter, inter.user, 'That channel is exempted already', view=self, interaction=True)
        bot_db.update_exempted_ids(inter.guild.id, bot_db.exempted_ids[inter.guild.id] + [channel.id])
        await slash_embed(
            inter,
            inter.user,
            f'Edited/deleted messages in {channel.mention} will no longer be logged',
            'Channel exempted',
            bot_db.embed_color[inter.guild.id],
            view=self,
            interaction=True
        )


class Exempt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(
        name='exempt',
        description='exempts a channel from logging',
        guild_ids=[GUILD_ID]
    )
    @discord.default_permissions(administrator=True)
    async def exempt(
        self,
        ctx,
        action: Option(
            name='action',
            description='Add or remove a channel from the exempt list',
            choices=['Add', 'Remove'],
            required=True
        ),
        channel: Option(
            discord.TextChannel,
            name='channel',
            description='channel to remove or add from the exempt list',
            required=True
        )
    ):
        if action == 'Add':
            if channel.id in bot_db.exempted_ids[ctx.guild.id]:
                return await slash_embed(ctx, ctx.author, 'That channel is exempted already')
            bot_db.update_exempted_ids(ctx.guild, bot_db.exempted_ids[ctx.guild.id] + [channel.id])
            await slash_embed(
                ctx,
                ctx.author,
                f'Edited/deleted messages in {channel.mention} will no longer be logged',
                'Channel exempted',
                bot_db.embed_color[ctx.guild.id],
                view=UndoAddExempt(self.bot)
            )
        if action == 'Remove':
            if channel.id not in bot_db.exempted_ids[ctx.guild.id]:
                return await slash_embed(ctx, ctx.author, 'That channel isn\'t exempted')
            exempt_list = bot_db.exempted_ids[ctx.guild.id]
            exempt_list.remove(channel.id)
            bot_db.update_exempted_ids(ctx.guild, exempt_list)
            await slash_embed(
                ctx,
                ctx.author,
                f'Edited/deleted messages in {channel.mention} will now be logged',
                'Channel un-exempted',
                bot_db.embed_color[ctx.guild.id],
                view=UndoRemoveExempt(self.bot)
            )

    @discord.slash_command(
        name='exempt-list',
        description='lists the exempted/un-exempted channels',
        guild_ids=[GUILD_ID]
    )
    @discord.default_permissions(administrator=True)
    async def exempt_list(
        self,
        ctx,
        action: Option(
            name='option',
            description='List the exempted or un-exempted channels',
            choices=['Exempted', 'Un-Exempted'],
            required=True
        )
    ):
        if action == 'Exempted':
            await slash_embed(
                ctx,
                ctx.author,
                f'<#{(">, <#".join(str(v) for v in bot_db.exempted_ids[ctx.guild.id]))}>',
                f'Exempted Channels ({len(bot_db.exempted_ids[ctx.guild.id])})',
                bot_db.embed_color[ctx.guild.id]
            )
        if action == 'Un-Exempted':
            exempted_chl = bot_db.exempted_ids[ctx.guild.id]
            channel_list = []
            for channel in ctx.guild.text_channels:
                if channel.id not in exempted_chl:
                    channel_list.append(str(channel.id))
            await slash_embed(
                ctx,
                ctx.author,
                f'<#{(">, <#".join(channel_list))}>',
                f'Un-Exempted Channels ({len(channel_list)})',
                bot_db.embed_color[ctx.guild.id]
            )

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(UndoAddExempt(self.bot))
        self.bot.add_view(UndoRemoveExempt(self.bot))


def setup(bot):
    bot.add_cog(Exempt(bot))
