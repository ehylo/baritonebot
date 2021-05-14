import logging
import main
from discord.ext import commands
from cogs.help import Help


class Response(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True, case_insensitive=True, aliases=['rp'])
    @commands.check(main.helper_group)
    async def response(self, ctx):
        await Help.response(self, ctx)

    @response.command(aliases=['l'])
    @commands.check(main.helper_group)
    async def list(self, ctx):
        main.cur.execute('SELECT ROW_NUMBER () OVER ( ORDER BY response_num ) rowNum, response_title, response_num FROM responses')
        responses = main.cur.fetchall()
        desc = ''
        for row in responses:
            desc += f'**{row[2]}.** {row[1]}\n'
        await main.channel_embed(ctx, f'Current Responses ({len(responses)}):', desc)

    @response.command(aliases=['d'])
    @commands.check(main.helper_group)
    async def details(self, ctx, rnum: int = None):
        if rnum is None:
            await main.error_embed(ctx, 'You need to give the response number to get the details')
        elif rnum <= 0:
            await main.error_embed(ctx, 'You need to give a **positive non zero** response number')
        else:
            main.cur.execute('SELECT * FROM responses WHERE response_num=%s', (rnum,))
            response = main.cur.fetchone()
            if response is not None:
                await main.help_embed(ctx, f'Response #{rnum} details:', f'`{response[0]}`', response[2], response[1])
            else:
                await main.error_embed(ctx, 'There is no response with that number yet')

    @response.command(aliases=['r'])
    @commands.check(main.mod_group)
    async def remove(self, ctx, rnum: int = None):
        if rnum is None:
            await main.error_embed(ctx, 'You need to give the response number to remove it')
        elif rnum <= 0:
            await main.error_embed(ctx, 'You need to give a **positive non zero** response number')
        else:
            main.cur.execute('SELECT response_num, response_title FROM responses WHERE response_num=%s', (rnum,))
            response = main.cur.fetchone()
            if response is not None:
                await main.channel_embed(ctx, f'Removed response #{rnum}:', response[1])
                logging.info(f'{ctx.author.id} removed response #{rnum}, \"{response[1]}\"')
                main.cur.execute('DELETE FROM responses WHERE response_num=%s', (rnum,))
                main.db.commit()
            else:
                await main.error_embed(ctx, 'There is no response with that number')

    @response.command(aliases=['a'])
    @commands.check(main.mod_group)
    async def add(self, ctx, eregex=None, etitle=None, *, edesc=None):
        if eregex is None:
            await main.error_embed(ctx, 'You need to give a regex')
        if etitle is None:
            await main.error_embed(ctx, 'You need to give a title')
        elif edesc is None:
            await main.error_embed(ctx, 'You need to give a description')
        else:
            main.cur.execute('SELECT * FROM responses')
            number = len(main.cur.fetchall())+1
            main.cur.execute('INSERT INTO responses(response_regex, response_title, response_description, response_num) VALUES(%s, %s, %s, %s)', (eregex, etitle, edesc, number))
            main.db.commit()
            await main.help_embed(ctx, 'New response:', f'`{eregex}`', edesc, etitle)
            logging.info(f'{ctx.author.id} added response with title: {etitle}')


def setup(bot):
    bot.add_cog(Response(bot))
