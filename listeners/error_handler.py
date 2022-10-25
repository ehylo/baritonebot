import traceback

import discord
from discord.ext import commands


class Errors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_error(self, error):
        exception = '\n'.join(traceback.format_exception(type(error), error, error.__traceback__))
        exception = f'```py\n{exception}```'
        print(exception)

    @commands.Cog.listener()
    async def on_application_command_error(self, inter: discord.Interaction, error):
        exception = '\n'.join(traceback.format_exception(type(error), error, error.__traceback__))
        print(exception)
        await inter.response.send_message('```py\n' + exception[:1990] + '```')


async def setup(bot):
    await bot.add_cog(Errors(bot))
