import discord
import logging
from discord.ext import commands
from cogs.help import Help
from cogs.const import help_embed, channel_embed, log_embed, logChannel, error_embed

class Optout(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def optout(self, ctx, *, arg=None):
        if arg == None:
            await Help.optout(self, ctx)
        elif arg == 'I am sure':
            #channel = await ctx.author.create_dm()
            #embedDm.description = ('We appreciate you opting out. You have been banned from the server to prevent bypassing our moderation system.')
            await ctx.guild.ban(user=ctx.author, reason='Opted out and banned', delete_message_days=7)
            desc = f'{ctx.author.mention} has been banned for reason: \n```User {ctx.author} has opted out```'
            title = 'User Banned'
            channel = await self.bot.fetch_channel(logChannel)
            await channel_embed(ctx, title, desc)
            await log_embed(ctx, title, desc, channel)
            logging.info(f'{ctx.author.id} has been banned for reason: Opted out')
        else:
            title = 'Opt-Out'
            desc = (f'You will be **banned from this server** and **lose all your roles** by continuing. Are you sure you want to opt out? if yes, type `b?optout I am sure`')
            await channel_embed(ctx, title, desc)

    @optout.error
    async def optout_error(self, ctx, error):
        desc = None
        await error_embed(ctx, desc, error)
        logging.info(f'{ctx.author.id} tried to optout but it gave the error: {error}')

def setup(bot):
    bot.add_cog(Optout(bot))