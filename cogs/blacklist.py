import discord
import logging
from discord.ext import commands
from cogs.help import Help
from cogs.const import helper_group, mod_group, error_embed, channel_embed

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
        num_lines = sum(1 for line in open("./data/blacklist.txt"))
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
                if num_lines == 0:
                    f.write(word)
                else:
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
                await error_embed(ctx, desc)

    @list.error
    @blacklist.error
    @add.error
    @remove.error
    async def blacklist_error(self, ctx, error):
        if isinstance(error, commands.errors.CheckFailure):
            pass
        else:
            desc = None
            await error_embed(ctx, desc, error)
            logging.info(f'{ctx.author.id} tried to use the command {ctx.command} but it gave the error: {error}')

def setup(bot):
    bot.add_cog(Blacklist(bot))