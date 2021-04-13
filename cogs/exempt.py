import discord
import logging
from cogs.help import Help
from discord.ext import commands
from cogs.const import error_embed, admin_group, channel_embed

class Exempt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    @commands.check(admin_group)
    async def exempt(self, ctx):
        num_lines = sum(1 for line in open("./data/exemptchannels.txt"))
        word = str(ctx.channel.id)
        f = open("./data/exemptchannels.txt", "r")
        lines = f.readlines()
        f.close()
        if num_lines == 0:
            f = open("./data/exemptchannels.txt", "a")
            f.write(f'{word}')
            f.close()
            title = 'Exempted'
            desc = f'The channel {ctx.channel.mention} is now exempted from the blacklist and regex responses'
            await channel_embed(ctx, title, desc)
            logging.info(f'{ctx.author.id} added a channel ({word}) to the exemptchannels')
        else:
            res = [sub.replace('\n', '') for sub in lines]
        if word not in res:
            f = open("./data/exemptchannels.txt", "a")
            f.write(f'\n{word}')
            f.close()
            title = 'Exempted'
            desc = f'The channel {ctx.channel.mention} is now exempted from the blacklist and regex responses'
            await channel_embed(ctx, title, desc)
            logging.info(f'{ctx.author.id} added a channel ({word}) to the exemptchannels')
        else:
            desc = 'This channel is already on the exempt list'
            await error_embed(ctx, desc)

    @exempt.command()
    @commands.check(admin_group)
    async def list(self, ctx):
        slist = open("./data/exemptchannels.txt", "r")
        mlist = []
        for line in slist:
            mchId = self.bot.get_channel(int(line))
            mlist.append(mchId.mention)
        jmlist = (', '.join(mlist))[1:-1]
        desc = f'<{jmlist}>'
        title = ('Exempted Channels')
        await channel_embed(ctx, title, desc)

    @exempt.command()
    @commands.check(admin_group)
    async def help(self, ctx):
        await Help.exempt(self, ctx)

    @exempt.error
    @help.error
    @list.error
    async def exempt_error(self, ctx, error):
        if isinstance(error, commands.errors.CheckFailure):
            pass
        else:
            desc = None
            await error_embed(ctx, desc, error)
            logging.info(f'{ctx.author.id} tried to use the command {ctx.command} but it gave the error: {error}')

class Unexempt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    @commands.check(admin_group)
    async def unexempt(self, ctx):
        num_lines = sum(1 for line in open("./data/exemptchannels.txt"))
        tlines = 1
        f = open("./data/exemptchannels.txt", "r")
        lines = f.readlines()
        res = [sub.replace('\n', '') for sub in lines]
        word = str(ctx.channel.id)
        if word in res:
            with open("./data/exemptchannels.txt", "r") as f:
                lines = f.readlines()
            with open("./data/exemptchannels.txt", "w") as f:
                for line in lines:
                    tlines += 1
                    if tlines == num_lines and (line.strip("\n") == word):
                        with open("./data/exemptchannels.txt", "r") as d:
                            llines = d.readlines()
                        with open("./data/exemptchannels.txt", "w") as d:
                            for lline in llines:
                                if tlines != num_lines and lline.strip("\n") != word:
                                    f.write(lline)
                                elif tlines == num_lines:
                                    sline = lline.strip('\n')
                                    f.write(sline)
                        d.close()
                    elif tlines != num_lines and line.strip("\n") != word:
                        f.write(line)
                    elif tlines == num_lines:
                        sline = line.strip('\n')
                        f.write(sline)
            title = 'Un-exempted'
            desc = (f'The channel {ctx.channel.mention} is no longer exempted from the blacklist and regex responses')
            await channel_embed(ctx, title, desc)
            logging.info(f'{ctx.author.id} removed a channel ({word}) from the exemptchannels')
            f.close()
        else:
            desc = 'This channel is not exempted'
            await error_embed(ctx, desc)
                
    @unexempt.command()
    @commands.check(admin_group)
    async def help(self, ctx):
        await Help.exempt(self, ctx)

    @unexempt.error
    @help.error
    async def exempt_error(self, ctx, error):
        if isinstance(error, commands.errors.CheckFailure):
            pass
        else:
            desc = None
            await error_embed(ctx, desc, error)
            logging.info(f'{ctx.author.id} tried to use the command {ctx.command} but it gave the error: {error}')

def setup(bot):
    bot.add_cog(Exempt(bot))
    bot.add_cog(Unexempt(bot))