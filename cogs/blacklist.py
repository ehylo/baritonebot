import discord
import logging
from discord.ext import commands
from cogs.help import Help
from cogs.const import helper_group, mod_group, error_embed, channel_embed, help_embed, admin_group

class Blacklist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    @commands.check(helper_group)
    async def blacklist(self, ctx):
        await Help.blacklist(self, ctx)

    @blacklist.command()
    @commands.check(helper_group)
    async def list(self, ctx):
        blist = open("./data/blacklist.txt", "r")
        desc = (f'```\n{blist.read()}```')
        blist.close()
        title = ('Blacklisted Words')
        await channel_embed(ctx, title, desc)
    
    @blacklist.command()
    @commands.check(mod_group)
    async def add(self, ctx, word=None):
        f = open("./data/blacklist.txt", "r")
        lines = f.readlines()
        res = [sub.replace('\n', '') for sub in lines]
        if word == None:
            desc = ('You need to give a word to add')
            await error_embed(ctx, desc)
        elif " " in word:
            desc = ('Do not add a space')
            await error_embed(ctx, desc)
        else:
            if word not in res:
                f = open("./data/blacklist.txt", "a")
                f.write(f'\n{word}')
                f.close()
                title = 'Added'
                desc = (f'The word `{word}` has been added to the blacklist')
                await channel_embed(ctx, title, desc)
                logging.info(f'{ctx.author.id} added a word to the blacklist')
            else:
                desc = 'That word already exists on the blacklist'
                await error_embed(ctx, desc)

    @blacklist.command()
    @commands.check(mod_group)
    async def remove(self, ctx, word=None):
        f = open("./data/blacklist.txt", "r")
        lines = f.readlines()
        res = [sub.replace('\n', '') for sub in lines]
        if word == None:
            desc = ('You need to give a word to remove')
            await error_embed(ctx, desc)
        else:
            if word in res:
                with open("./data/blacklist.txt", "r") as f:
                    lines = f.readlines()
                with open("./data/blacklist.txt", "w") as f:
                    for line in lines:
                        if line.strip("\n") != word:
                            f.write(line)
                title = 'Removed'
                desc = (f'The word `{word}` has been removed from the blacklist')
                await channel_embed(ctx, title, desc)
                logging.info(f'{ctx.author.id} removed a word from the blacklist')
            else:
                desc = 'That word is not in the blacklist'
                error_embed(ctx, desc)

    @commands.command()
    @commands.check(admin_group)
    async def exempt(self, ctx, elp=None):
        if elp == 'help':
            await Help.exempt(self, ctx)
        elif elp == 'list':
            slist = open("./data/exemptchannels.txt", "r")
            #desc = (f'```\n{mlist.read()}```')
            #slist.close()
            mlist = []
            for line in slist:
                mchId = self.bot.get_channel(int(line))
                mlist.append(mchId.mention)
            jmlist = (', '.join(mlist))[1:-1]
            desc = f'<{jmlist}>'
            title = ('Exempted Channels')
            await channel_embed(ctx, title, desc)
        else:
            word = str(ctx.channel.id)
            f = open("./data/exemptchannels.txt", "r")
            lines = f.readlines()
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

    @commands.command()
    @commands.check(admin_group)
    async def unexempt(self, ctx, elp=None):
        f = open("./data/exemptchannels.txt", "r")
        lines = f.readlines()
        res = [sub.replace('\n', '') for sub in lines]
        if elp == 'help':
            await Help.exempt(self, ctx)
        else:
            word = ctx.channel.id
            if word in res:
                with open("./data/exemptchannels.txt", "r") as f:
                    lines = f.readlines()
                with open("./data/exemptchannels.txt", "w") as f:
                    for line in lines:
                        if line.strip("\n") != str(word):
                            f.write(line)
                title = 'Un-exempted'
                desc = (f'The channel {ctx.channel.mention} is no longer exempted from the blacklist and regex responses')
                await channel_embed(ctx, title, desc)
                logging.info(f'{ctx.author.id} removed a channel ({word}) from the exemptchannels')
            else:
                desc = 'That channel is not exempted'
                error_embed(ctx, desc)

    @list.error
    @blacklist.error
    async def listhelp_error(self, ctx, error):
        if isinstance(error, commands.errors.CheckFailure):
            desc = (f'You need to be a Helper to use the command `{ctx.command}`')
            await error_embed(ctx, desc)
        else:
            desc = None
            await error_embed(ctx, desc, error)
            logging.info(f'{ctx.author.id} tried to list the blacklisted words but it gave the error: {error}')

    @add.error
    @remove.error
    async def addremove_error(self, ctx, error):
        if isinstance(error, commands.errors.CheckFailure):
            desc = (f'You need to be a Moderator to use the command `{ctx.command}`')
            await error_embed(ctx, desc)
        else:
            desc = None
            await error_embed(ctx, desc, error)
            logging.info(f'{ctx.author.id} tried to add/remove word from blacklist but it gave the error: {error}')
    
    @exempt.error
    @unexempt.error
    async def exempt_error(self, ctx, error):
        if isinstance(error, commands.errors.CheckFailure):
            desc = (f'You need to be an Admin to use the command `{ctx.command}`')
            await error_embed(ctx, desc)
        else:
            desc = None
            await error_embed(ctx, desc, error)
            logging.info(f'{ctx.author.id} tried to add/remove channel to the exemptchannels but it gave the error: {error}')

def setup(bot):
    bot.add_cog(Blacklist(bot))