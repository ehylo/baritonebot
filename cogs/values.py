import discord
import logging
from discord.ext import commands
from cogs.help import Help
from const import channel_embed, admin_group, mod_group, baritoneDiscord, cur, db


class Prefix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True, case_insensitive=True, aliases=['pf'])
    @commands.check(admin_group)
    async def prefix(self, ctx, fixpre=None):
        if fixpre is None:
            await Help.prefix(self, ctx)
        else:
            cur.execute(f'UPDATE settings SET prefix={fixpre}')
            db.commit()
            await channel_embed(ctx, 'Prefix set', f'Set the prefix to {fixpre}, please restart the bot for the changes to take affect')
            logging.info(f'{ctx.author.id} set the prefix to {fixpre}')

    @prefix.command(aliases=['d'])
    @commands.check(admin_group)
    async def default(self, ctx):
        cur.execute('UPDATE settings SET prefix="b?"')
        db.commit()
        await channel_embed(ctx, 'Prefix set', 'Set the prefix to the default (b?), please restart the bot for the changes to take affect')
        logging.info(f'{ctx.author.id} set the prefix to default')


class EmbedColor(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True, case_insensitive=True, aliases=['ec'])
    @commands.check(admin_group)
    async def embedcolor(self, ctx, color=None):
        if color is None:
            await Help.embedcolor(self, ctx)
        else:
            cur.execute(f'UPDATE settings SET embedcolor={color}')
            db.commit()
            await channel_embed(ctx, 'Embedcolor set', f'Set the embed color to {color}, please restart the bot for the changes to take affect')
            logging.info(f'{ctx.author.id} set the embedcolor to {color}')

    @embedcolor.command(aliases=['d'])
    @commands.check(admin_group)
    async def default(self, ctx):
        cur.execute('UPDATE settings SET embedcolor="81C3FF"')
        db.commit()
        await channel_embed(ctx, 'Embedcolor set', 'Set the embed color to the default (81C3FF), please restart the bot for the changes to take affect')
        logging.info(f'{ctx.author.id} set the embedcolor to default')


class Nick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True, case_insensitive=True, aliases=['n'])
    @commands.check(mod_group)
    async def nick(self, ctx, *, name=None):
        b_guild = self.bot.get_guild(baritoneDiscord)
        if name is None:
            await Help.nick(self, ctx)
        else:
            await b_guild.me.edit(nick=name)
            await channel_embed(ctx, 'Nick set', f'Set the bot\'s nickname in this server to `{name}`')
            logging.info(f'{ctx.author.id} set the nick to {name}')

    @nick.command(aliases=['d'])
    @commands.check(mod_group)
    async def default(self, ctx):
        b_guild = self.bot.get_guild(baritoneDiscord)
        await b_guild.me.edit(nick='Franky')
        await channel_embed(ctx, 'Nick set', 'Set the bot\'s nickname in this server to the default (Franky)')
        logging.info(f'{ctx.author.id} set the nick to default')

    @nick.command(aliases=['r'])
    @commands.check(mod_group)
    async def remove(self, ctx):
        b_guild = self.bot.get_guild(baritoneDiscord)
        await b_guild.me.edit(nick=None)
        await channel_embed(ctx, 'Nick removed', 'Removed the bot\'s nick in this server')
        logging.info(f'{ctx.author.id} removed the nick')


class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True, case_insensitive=True, aliases=['s'])
    @commands.check(mod_group)
    async def status(self, ctx, *, presence=None):
        if presence is None:
            await Help.status(self, ctx)
        else:
            cur.execute(f'UPDATE settings SET presence={presence}')
            db.commit()
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=presence))
            await channel_embed(ctx, 'Presence set', f'Set the presence to `Watching {presence}`.')
            logging.info(f'{ctx.author.id} set the status to {presence}')

    @status.command(aliases=['d'])
    @commands.check(mod_group)
    async def default(self, ctx):
        cur.execute('UPDATE settings SET presence="humans interact"')
        db.commit()
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='humans interact'))
        await channel_embed(ctx, 'Presence set', 'Set the presence to the default (`Watching humans interact`).')
        logging.info(f'{ctx.author.id} set the presence to default')


def setup(bot):
    bot.add_cog(Prefix(bot))
    bot.add_cog(EmbedColor(bot))
    bot.add_cog(Nick(bot))
    bot.add_cog(Status(bot))
