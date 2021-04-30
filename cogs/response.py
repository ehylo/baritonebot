import logging
from discord.ext import commands
from cogs.help import Help
from const import error_embed, channel_embed, helper_group, mod_group, help_embed, cur, db


class Response(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True, case_insensitive=True, aliases=['rp'])
    @commands.check(helper_group)
    async def response(self, ctx):
        await Help.response(self, ctx)

    @response.command(aliases=['l'])
    @commands.check(helper_group)
    async def list(self, ctx):
        cur.execute('SELECT ROW_NUMBER () OVER ( ORDER BY response_num ) rowNum, response_title, response_num FROM responses')
        responses = cur.fetchall()
        desc = ''
        for row in responses:
            desc += f'**{row[2]}.** {row[1]}\n'
        await channel_embed(ctx, f'Current Responses ({len(responses)}):', desc)

    @response.command(aliases=['d'])
    @commands.check(helper_group)
    async def details(self, ctx, rnum: int = None):
        if rnum is None:
            await error_embed(ctx, 'You need to give the response number to get the details')
        elif rnum <= 0:
            await error_embed(ctx, 'You need to give a **positive non zero** response number')
        else:
            cur.execute('SELECT * FROM responses WHERE response_num=%s', (rnum,))
            response = cur.fetchone()
            if response is not None:
                await help_embed(ctx, f'Response #{rnum} details:', f'`{response[0]}`', response[2], response[1])
            else:
                await error_embed(ctx, 'There is no response with that number yet')

    @response.command(aliases=['r'])
    @commands.check(mod_group)
    async def remove(self, ctx, rnum: int = None):
        if rnum is None:
            await error_embed(ctx, 'You need to give the response number to remove it')
        elif rnum <= 0:
            await error_embed(ctx, 'You need to give a **positive non zero** response number')
        else:
            cur.execute('SELECT response_num, response_title FROM responses WHERE response_num=%s', (rnum,))
            response = cur.fetchone()
            if response is not None:
                await channel_embed(ctx, f'Removed response #{rnum}:', response[1])
                logging.info(f'{ctx.author.id} removed response #{rnum}, \"{response[1]}\"')
                cur.execute('DELETE FROM responses WHERE response_num=%s', (rnum,))
                db.commit()
            else:
                await error_embed(ctx, 'There is no response with that number')

    @response.command(aliases=['a'])
    @commands.check(mod_group)
    async def add(self, ctx, eregex=None, etitle=None, *, edesc=None):
        if eregex is None:
            await error_embed(ctx, 'You need to give a regex')
        if etitle is None:
            await error_embed(ctx, 'You need to give a title')
        elif edesc is None:
            await error_embed(ctx, 'You need to give a description')
        else:
            cur.execute('SELECT * FROM responses')
            number = len(cur.fetchall())+1
            cur.execute('INSERT INTO responses(response_regex, response_title, response_description, response_num) VALUES(%s, %s, %s, %s)', (eregex, etitle, edesc, number))
            db.commit()
            await help_embed(ctx, 'New response:', f'`{eregex}`', edesc, etitle)
            logging.info(f'{ctx.author.id} added response with title: {etitle}')


def setup(bot):
    bot.add_cog(Response(bot))
