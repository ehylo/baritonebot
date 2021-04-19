import logging
from cogs.help import Help
from discord.ext import commands
from const import helper_group, mod_group, error_embed, channel_embed


class Blacklist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True, case_insensitive=True, aliases=['bl'])
    @commands.check(helper_group)
    async def blacklist(self, ctx):
        await Help.blacklist(self, ctx)

    @blacklist.command(aliases=['l'])
    @commands.check(helper_group)
    async def list(self, ctx):
        blist = open("./data/blacklist.txt", "r")
        desc = f'```\n{blist.read()}```'
        blist.close()
        await channel_embed(ctx, 'Blacklisted Words', desc)
    
    @blacklist.command(aliases=['a'])
    @commands.check(mod_group)
    async def add(self, ctx, word=None):
        f = open("./data/blacklist.txt", "r")
        if word is None:
            await error_embed(ctx, 'You need to give a word to add')
        elif ' ' in word:
            await error_embed(ctx, 'Do not add a space')
        else:
            if word not in [sub.replace('\n', '') for sub in (f.readlines())]:
                f = open("./data/blacklist.txt", "a")
                if (sum(1 for _ in open("./data/blacklist.txt"))) == 0:
                    f.write(word)
                else:
                    f.write(f'\n{word}')
                f.close()
                await channel_embed(ctx, 'Added', f'The word `{word}` has been added to the blacklist')
                logging.info(f'{ctx.author.id} added a word to the blacklist')
            else:
                await error_embed(ctx, 'That word already exists on the blacklist')

    @blacklist.command(aliases=['r'])
    @commands.check(mod_group)
    async def remove(self, ctx, word=None):
        f = open("./data/blacklist.txt", "r")
        if word is None:
            await error_embed(ctx, 'You need to give a word to remove')
        else:
            if word in [sub.replace('\n', '') for sub in (f.readlines())]:
                with open("./data/blacklist.txt", "r") as f:
                    lines = f.readlines()
                with open("./data/blacklist.txt", "w") as f:
                    for line in lines:
                        if line.strip("\n") != word:
                            f.write(line)
                await channel_embed(ctx, 'Removed', f'The word `{word}` has been removed from the blacklist')
                logging.info(f'{ctx.author.id} removed a word from the blacklist')
            else:
                await error_embed(ctx, 'That word is not in the blacklist')


def setup(bot):
    bot.add_cog(Blacklist(bot))
