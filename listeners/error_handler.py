import traceback
import logging

import discord
from discord.ext import commands

log = logging.getLogger('listeners.error_handler')


class Errors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_error(self, error):
        exception = '\n'.join(traceback.format_exception(type(error), error, error.__traceback__))
        log.error(exception)

    @commands.Cog.listener()
    async def on_application_command_error(self, inter: discord.Interaction, error):
        exception = '\n'.join(traceback.format_exception(type(error), error, error.__traceback__))
        log.error(exception)
        await inter.response.send_message('An unhandled exception has occurred.')


async def setup(bot):
    await bot.add_cog(Errors(bot))
