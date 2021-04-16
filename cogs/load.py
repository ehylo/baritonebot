import logging
from discord.ext import commands
from cogs.help import Help
from const import admin_group, channel_embed


class Load(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.check(admin_group)
    async def load(self, ctx, extension=None):
        if extension is None:
            await Help.load(self, ctx)
        else:
            self.bot.load_extension(f'cogs.{extension}')
            await channel_embed(ctx, 'Loaded Extension', f'The extension {extension} has been loaded')
            logging.info(f'{ctx.author.id} loaded the extension {extension}')

    @commands.command()
    @commands.check(admin_group)
    async def unload(self, ctx, extension=None):
        if extension is None:
            await Help.unload(self, ctx)
        else:
            self.bot.unload_extension(f'cogs.{extension}')
            await channel_embed(ctx, 'Unloaded Extension', f'The extension {extension} has been unloaded')
            logging.info(f'{ctx.author.id} unloaded the extension {extension}')

    @commands.command()
    @commands.check(admin_group)
    async def reload(self, ctx, extension=None):
        if extension is None:
            await Help.reload(self, ctx)
        else:
            self.bot.unload_extension(f'cogs.{extension}')
            self.bot.load_extension(f'cogs.{extension}')
            await channel_embed(ctx, 'Reloaded Extension', f'The extension {extension} has been reloaded')
            logging.info(f'{ctx.author.id} reloaded the extension {extension}')


def setup(bot):
    bot.add_cog(Load(bot))
