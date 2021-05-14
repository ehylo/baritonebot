import os
import main
from discord.ext import commands
from cogs.help import Help


class Extension(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True, case_insensitive=True, aliases=['ext'])
    @commands.check(main.admin_group)
    async def extension(self, ctx):
        await Help.extension(self, ctx)

    @extension.command(aliases=['ld'])
    @commands.check(main.admin_group)
    async def load(self, ctx, extension=None):
        if extension is None:
            await main.error_embed(ctx, 'You need to give an extenstion to load (do `extension list` for a list of extensions')
        else:
            if extension == 'all':
                for filename in os.listdir('./cogs'):
                    if filename.endswith('.py'):
                        self.bot.load_extension(f'cogs.{filename[:-3]}')
            else:
                try:
                    self.bot.load_extension(f'cogs.{extension}')
                    await main.channel_embed(ctx, 'Loaded Extension', f'The extension {extension} has been loaded')
                    print(f'{ctx.author.id} loaded the extension {extension}')
                except commands.ExtensionNotFound:
                    await main.error_embed(ctx, 'That is not a valid extension, use `extension list` to see all available extensions')
                except commands.ExtensionAlreadyLoaded:
                    await main.error_embed(ctx, 'That extension is already loaded')

    @extension.command(aliases=['u'])
    @commands.check(main.admin_group)
    async def unload(self, ctx, extension=None):
        if extension is None:
            await main.error_embed(ctx, 'You need to give an extenstion to unload (do `extension list` for a list of extensions')
        else:
            if extension == 'all':
                for filename in os.listdir('./cogs'):
                    if filename.endswith('.py'):
                        self.bot.unload_extension(f'cogs.{filename[:-3]}')
            else:
                try:
                    self.bot.unload_extension(f'cogs.{extension}')
                    await main.channel_embed(ctx, 'Unloaded Extension', f'The extension {extension} has been unloaded')
                    print(f'{ctx.author.id} unloaded the extension {extension}')
                except commands.ExtensionNotFound:
                    await main.error_embed(ctx, 'That is not a valid extension, use `extension list` to see all available extensions')
                except commands.ExtensionNotLoaded:
                    await main.error_embed(ctx, 'That extension is already unloaded')

    @extension.command(aliases=['r'])
    @commands.check(main.admin_group)
    async def reload(self, ctx, extension=None):
        if extension is None:
            await main.error_embed(ctx, 'You need to give an extenstion to reload (do `extension list` for a list of extensions')
        else:
            if extension == 'all':
                for filename in os.listdir('./cogs'):
                    if filename.endswith('.py'):
                        self.bot.reload_extension(f'cogs.{filename[:-3]}')
            else:
                try:
                    self.bot.reload_extension(f'cogs.{extension}')
                    await main.channel_embed(ctx, 'Reloaded Extension', f'The extension {extension} has been reloaded')
                    print(f'{ctx.author.id} reloaded the extension {extension}')
                except commands.ExtensionNotFound:
                    await main.error_embed(ctx, 'That is not a valid extension, use `extension list` to see all available extensions')

    @extension.command(aliases=['l'])
    @commands.check(main.admin_group)
    async def list(self, ctx):
        desc = '\
            \u2022 **`event`** - blacklist, regex responses, paste upload, dm log, invite delete, nick changer, 24h log clear, message edit/delete, member join/leave, join/leave voice, and error handler \
            \n\u2022 **`values`** - `embedcolor`, `status`, `prefix`, and `nick` commands \
            \n\u2022 **`bkm`** - `mute`, `ban`, `kick`, `unban`, and `unmute` commands \
            \n\u2022 **`misc`** - `ping`, `rps`, and `flip` commands \
            \n\u2022 **`info`** - `serverinfo` and `userinfo` commands \
            \n\u2022 **`role`** - `ignore` and `releases` commands \
            \n\u2022 **`optout`** - command \
            \n\u2022 **`response`** - command \
            \n\u2022 **`rule`** - command \
            \n\u2022 **`blacklist`** - command \
            \n\u2022 **`clear`** - command \
            \n\u2022 **`cringe`** - command \
            \n\u2022 **`embed`** - command \
            \n\u2022 **`emote`** - command \
            \n\u2022 **`exempt`** - command \
            \n\u2022 **`help`** - commands'
        await main.channel_embed(ctx, 'All Extensions:', desc)


def setup(bot):
    bot.add_cog(Extension(bot))
