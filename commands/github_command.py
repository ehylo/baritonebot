from discord.ext import commands


class GithubCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(GithubCommand(bot))
