import discord
import os
import sys
import json
import logging
from discord.ext import commands
from cogs.help import Help
from cogs.const import valuesStr, preCmd, setNick, setPresence, error_embed, help_embed, channel_embed, admin_group, mod_group

class Prefix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    @commands.check(admin_group)
    async def prefix(self, ctx, fixpre=None):
        if fixpre == None:
            await Help.prefix(self, ctx)
        else:
            for item in valuesStr:
                item['prefix'] = fixpre
            with open((os.path.join(sys.path[0], './data/values.json')), 'w') as file:
                json.dump(valuesStr, file, indent=2)
                title = 'Prefix set'
                desc = (f'Set the prefix to {fixpre}, please restart the bot for the changes to take affect')
                await channel_embed(ctx, title, desc)
                logging.info(f'{ctx.author.id} set the prefix to {fixpre}')

    @prefix.command()
    @commands.check(admin_group)
    async def default(self, ctx):
        for item in valuesStr:
            item['prefix'] = "b?"
        with open((os.path.join(sys.path[0], './data/values.json')), 'w') as file:
            json.dump(valuesStr, file, indent=2)
            title = 'Prefix set'
            desc = (f'Set the prefix to the default (b?), please restart the bot for the changes to take affect')
            await channel_embed(ctx, title, desc)
            logging.info(f'{ctx.author.id} set the prefix to default')

    @prefix.error
    @default.error
    async def status_error(self, ctx, error):
        if isinstance(error, commands.errors.CheckFailure):
            desc = (f'You need to be an Admin to use the command `{ctx.command}`')
            await error_embed(ctx, desc)
        else:
            desc = None
            await error_embed(ctx, desc, error)
            logging.info(f'{ctx.author.id} tried to set the prefix but it gave the error: {error}')

class EmbedColor(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    @commands.check(admin_group)
    async def embedcolor(self, ctx, color=None):
        if color == None:
            await Help.embedcolor(self, ctx)
        else:
            for item in valuesStr:
                item['color'] = color
            with open((os.path.join(sys.path[0], './data/values.json')), 'w') as file:
                json.dump(valuesStr, file, indent=2)
                title = 'Embedcolor set'
                desc = (f'Set the embed color to {color}, please restart the bot for the changes to take affect')
                await channel_embed(ctx, title, desc)
                logging.info(f'{ctx.author.id} set the embedcolor to {color}')

    @embedcolor.command()
    @commands.check(admin_group)
    async def default(self, ctx):
        for item in valuesStr:
            item['color'] = "81C3FF"
        with open((os.path.join(sys.path[0], './data/values.json')), 'w') as file:
            json.dump(valuesStr, file, indent=2)
            title = 'Embedcolor set'
            desc = (f'Set the embed color to the default (81C3FF), please restart the bot for the changes to take affect')
            await channel_embed(ctx, title, desc)
            logging.info(f'{ctx.author.id} set the embedcolor to default')

    @embedcolor.error
    @default.error
    async def status_error(self, ctx, error):
        if isinstance(error, commands.errors.CheckFailure):
            desc = (f'You need to be an Admin to use the command `{ctx.command}`')
            await error_embed(ctx, desc)
        else:
            desc = None
            await error_embed(ctx, desc, error)
            logging.info(f'{ctx.author.id} tried to set the embedcolor but it gave the error: {error}')

class Nick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    @commands.check(mod_group)
    async def nick(self, ctx, *, name=None):
        if name == None:
            await Help.nick(self, ctx)
        else:
            await ctx.guild.me.edit(nick=name)
            title = 'Nick set'
            desc = (f'Set the bot\'s nickname in this server to `{name}`')
            await channel_embed(ctx, title, desc)
            logging.info(f'{ctx.author.id} set the nick to {name}')

    @nick.command()
    @commands.check(mod_group)
    async def default(self, ctx):
        await ctx.guild.me.edit(nick=setNick)
        title = 'Nick set'
        desc = (f'Set the bot\'s nickname in this server to the default ({setNick})')
        await channel_embed(ctx, title, desc)
        logging.info(f'{ctx.author.id} set the nick to default')

    @nick.command()
    @commands.check(mod_group)
    async def remove(self, ctx):
        await ctx.guild.me.edit(nick=None)
        title = 'Nick removed'
        desc = (f'Removed the bot\'s nick in this server')
        await channel_embed(ctx, title, desc)
        logging.info(f'{ctx.author.id} removed the nick')

    @nick.error
    @default.error
    @remove.error
    async def nick_error(self, ctx, error):
        if isinstance(error, commands.errors.CheckFailure):
            desc = (f'You need to be a Moderator to use the command `{ctx.command}`')
            await error_embed(ctx, desc)
        else:
            desc = None
            await error_embed(ctx, desc, error)
            logging.info(f'{ctx.author.id} tried to remove/set the nick but it gave the error: {error}')

class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    @commands.check(mod_group)
    async def status(self, ctx, *, presence=None):
        if presence == None:
            await Help.status(self, ctx)
        else:
            for item in valuesStr:
                item['presence'] = presence
            with open((os.path.join(sys.path[0], './data/values.json')), 'w') as file:
                json.dump(valuesStr, file, indent=2)
            title = 'Presence set'
            desc = (f'Set the presence to `Watching {presence}`.')
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=presence))
            await channel_embed(ctx, title, desc)
            logging.info(f'{ctx.author.id} set the status to {presence}')

    @status.command()
    @commands.check(mod_group)
    async def default(self, ctx):
        for item in valuesStr:
            item['presence'] = 'humans interact'
        with open((os.path.join(sys.path[0], './data/values.json')), 'w') as file:
            json.dump(valuesStr, file, indent=2)
        desc = (f'Set the presence to the default (`Watching humans interact`).')
        title = 'Presence set'
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='humans interact'))
        await channel_embed(ctx, title, desc)
        logging.info(f'{ctx.author.id} set the presence to default')

    @status.error
    @default.error
    async def status_error(self, ctx, error):
        if isinstance(error, commands.errors.CheckFailure):
            desc = (f'You need to be a Moderator to use the command `{ctx.command}`')
            await error_embed(ctx, desc)
        else:
            desc = None
            await error_embed(ctx, desc, error)
            logging.info(f'{ctx.author.id} tried to set the status but it gave the error: {error}')

def setup(bot):
    bot.add_cog(Prefix(bot))
    bot.add_cog(EmbedColor(bot))
    bot.add_cog(Nick(bot))
    bot.add_cog(Status(bot))