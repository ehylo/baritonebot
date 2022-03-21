from discord.ext import commands


class MessageInteraction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(MessageInteraction(bot))
