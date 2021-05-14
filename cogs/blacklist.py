import logging
from cogs.help import Help
from discord.ext import commands
from main import helper_group, mod_group, error_embed, channel_embed, cur, db


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
        cur.execute('SELECT blacklist_word FROM blacklist')
        await channel_embed(ctx, 'Blacklisted Words', '```\n'+'\n'.join([item[0] for item in cur.fetchall()])+'```')

    @blacklist.command(aliases=['a'])
    @commands.check(mod_group)
    async def add(self, ctx, word=None):
        if word is None:
            await error_embed(ctx, 'You need to give a word to add')
        elif ' ' in word:
            await error_embed(ctx, 'Do not add a space')
        else:
            cur.execute('SELECT blacklist_word FROM blacklist WHERE blacklist_word=%s', (word,))
            if cur.fetchone() is None:
                cur.execute('INSERT INTO blacklist(blacklist_word) VALUES(%s)', (word,))
                db.commit()
                await channel_embed(ctx, 'Added', f'The word `{word}` has been added to the blacklist')
                logging.info(f'{ctx.author.id} added a word to the blacklist')
            else:
                await error_embed(ctx, 'That word already exists on the blacklist')

    @blacklist.command(aliases=['r'])
    @commands.check(mod_group)
    async def remove(self, ctx, word=None):
        if word is None:
            await error_embed(ctx, 'You need to give a word to remove')
        else:
            cur.execute('SELECT blacklist_word FROM blacklist WHERE blacklist_word=%s', (word,))
            if cur.fetchone() is not None:
                cur.execute('DELETE FROM blacklist WHERE blacklist_word=%s', (word,))
                db.commit()
                await channel_embed(ctx, 'Removed', f'The word `{word}` has been removed from the blacklist')
                logging.info(f'{ctx.author.id} removed a word from the blacklist')
            else:
                await error_embed(ctx, 'That word is not in the blacklist')


def setup(bot):
    bot.add_cog(Blacklist(bot))
