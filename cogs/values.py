import main
import discord
from discord.ext import commands
from cogs.help import Help


class Values(commands.Cog):
    def __init__(self, bot):
        """Returns embeds for all the values commands."""
        self.bot = bot

    @commands.group(invoke_without_command=True, case_insensitive=True, aliases=['pf'])
    @commands.check(main.admin_group)
    async def prefix(self, ctx, fixpre=None):
        if fixpre is None:
            return await Help.prefix(self, ctx)
        main.cur.execute("UPDATE settings SET prefix = %s WHERE yes='yes'", (fixpre,))
        main.db.commit()
        await main.channel_embed(ctx, 'Prefix set', f'Set the prefix to {fixpre}')
        print(f'{ctx.author.id} set the prefix to {fixpre}')

    @prefix.command(aliases=['d', 'default'])
    @commands.check(main.admin_group)
    async def defaultp(self, ctx):
        main.cur.execute("UPDATE settings SET prefix='b?' WHERE yes='yes'")
        main.db.commit()
        await main.channel_embed(ctx, 'Prefix set', 'Set the prefix to the default (b?)')
        print(f'{ctx.author.id} set the prefix to default')

    @commands.group(invoke_without_command=True, case_insensitive=True, aliases=['ec'])
    @commands.check(main.admin_group)
    async def embedcolor(self, ctx, color=None):
        if color is None:
            return await Help.embedcolor(self, ctx)
        main.cur.execute("UPDATE settings SET embedcolor = %s WHERE yes='yes'", (color,))
        main.db.commit()
        await main.channel_embed(ctx, 'Embedcolor set', f'Set the embed color to {color}')
        print(f'{ctx.author.id} set the embedcolor to {color}')

    @embedcolor.command(aliases=['d'])
    @commands.check(main.admin_group)
    async def defaulte(self, ctx):
        main.cur.execute("UPDATE settings SET embedcolor='81C3FF' WHERE yes='yes'")
        main.db.commit()
        await main.channel_embed(ctx, 'Embedcolor set', 'Set the embed color to the default (81C3FF)')
        print(f'{ctx.author.id} set the embedcolor to default')

    @commands.group(invoke_without_command=True, case_insensitive=True, aliases=['s'])
    @commands.check(main.mod_group)
    async def status(self, ctx, ptype: int = None, *, presence=None):
        if (ptype is None) or (presence is None):
            return await Help.status(self, ctx)
        if (ptype <= 0) or (ptype > 4):
            await main.error_embed(ctx, 'You need to give a number between 1 and 4 for the presence type, see `help status` for what each is')
        else:
            if ptype == 1:
                atype = discord.ActivityType.watching
                dtype = 'Watching'
            elif ptype == 2:
                atype = discord.ActivityType.playing
                dtype = 'Playing'
            elif ptype == 3:
                atype = discord.ActivityType.listening
                dtype = 'Listening to'
            else:
                atype = discord.ActivityType.competing
                dtype = 'Competing in'
            main.cur.execute("UPDATE settings SET presence = %s WHERE yes='yes'", (presence,))
            main.cur.execute("UPDATE settings SET presencetype = %s WHERE yes='yes'", (dtype,))
            main.db.commit()
            await self.bot.change_presence(activity=discord.Activity(type=atype, name=presence))
            await main.channel_embed(ctx, 'Presence set', f'Set the presence to `{dtype} {presence}`.')
            print(f'{ctx.author.id} set the status to {dtype} {presence}')

    @status.command(aliases=['d'])
    @commands.check(main.mod_group)
    async def defaults(self, ctx):
        main.cur.execute("UPDATE settings SET presence='humans interact' WHERE yes='yes'")
        main.cur.execute("UPDATE settings SET presencetype='Watching' WHERE yes='yes'")
        main.db.commit()
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='humans interact'))
        await main.channel_embed(ctx, 'Presence set', 'Set the presence to the default (`Watching humans interact`).')
        print(f'{ctx.author.id} set the presence to default')


def setup(bot):
    bot.add_cog(Values(bot))
