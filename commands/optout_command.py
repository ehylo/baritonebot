import discord
from discord.ext import commands

from utils import embeds


class OptOut(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name='opt-out', description='ban yourself from this server')
    @discord.app_commands.describe(
        confirmation='Type \"I am sure\" to confirm you want to ban yourself, this cannot be undone'
    )
    async def opt_out(self, inter: discord.Interaction, confirmation: str):
        if confirmation != 'I am sure':
            return await embeds.slash_embed(
                inter,
                inter.user,
                'You will be **banned from this server** and **lose all your roles** by continuing. '
                'If you are sure this is what you desire, confirm with "I am sure".'
            )
        await embeds.slash_embed(
            inter,
            inter.user,
            f'{inter.user.mention} has been banned by themself',
            'Member Banned',
            self.bot.db.embed_color[inter.guild.id],
            ephemeral=False
        )
        await embeds.mod_log_embed(
            self.bot,
            self.bot.db,
            inter.guild.id,
            inter.user,
            inter.user,
            'Member Banned',
            f'{inter.user.mention} has been banned by themself'
        )
        dm_channel = await inter.user.create_dm()
        await embeds.dm_embed(
            self.bot.db,
            inter.guild.id,
            channel=dm_channel,
            author=inter.user,
            title='Banned',
            description=f'You have been banned in the baritone discord because you chose to be'
        )
        await inter.user.ban(reason='Opted-out', delete_message_days=0)


async def setup(bot):
    await bot.add_cog(OptOut(bot))
