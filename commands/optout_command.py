import discord
from discord.ext import commands
from discord.commands import Option

from main import bot_db
from utils.const import GUILD_ID
from utils import embeds


class OptOut(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(
        name='opt-out', description='ban yourself from this server', guild_ids=[GUILD_ID]
    )
    async def opt_out(
        self,
        ctx,
        confirm: Option(
            str,
            name='confirmation',
            description='Type "I am sure" to confirm you want to ban yourself, this cannot be undone',
            required=True
        )
    ):
        if confirm != 'I am sure':
            return await embeds.slash_embed(
                ctx,
                ctx.author,
                'You will be **banned from this server** and **lose all your roles** by continuing. If you are sure this is what you desire, confirm with "I am sure".'
            )
        await embeds.slash_embed(
            ctx,
            ctx.author,
            f'{ctx.author.mention} has been banned by themself',
            'Member Banned',
            bot_db.embed_color[ctx.guild.id],
            ephemeral=False
        )
        await embeds.mod_log_embed(
            self.bot,
            bot_db,
            ctx.guild.id,
            ctx.author,
            ctx.author,
            'Member Banned',
            f'{ctx.author.mention} has been banned by themself'
        )
        dm_channel = await ctx.author.create_dm()
        await embeds.dm_embed(
            bot_db,
            ctx.guild.id,
            channel=dm_channel,
            author=ctx.author,
            title='Banned',
            description=f'You have been banned in the baritone discord because you chose to be'
        )
        await ctx.author.ban(reason='Opted-out', delete_message_days=0)


def setup(bot):
    bot.add_cog(OptOut(bot))
