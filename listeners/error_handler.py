import traceback

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
    async def on_application_command_error(self, _ctx, error):
        exception = '\n'.join(traceback.format_exception(type(error), error, error.__traceback__))
        exception = f'```py\n{exception}```'
        print(exception)


def setup(bot):
    bot.add_cog(Errors(bot))
