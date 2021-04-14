import logging
import json
from discord.ext import commands
from cogs.help import Help
from cogs.const import error_embed, channel_embed, helper_group, mod_group, help_embed, console


class Response(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    @commands.check(helper_group)
    async def response(self, ctx):
        await Help.response(ctx)

    @response.command()
    @commands.check(helper_group)
    async def list(self, ctx):
        with open('./data/responses.json') as jsonResp:
            response_list = json.load(jsonResp)
        desc = ''
        for x in range(1, (len(response_list) + 1)):
            desc += f'**{x}.** {(response_list[x - 1]["title"])}\n'
        await channel_embed(ctx, 'Current Responses:', desc)

    @response.command()
    @commands.check(helper_group)
    async def details(self, ctx, rnum: int = None):
        if rnum is None:
            await error_embed(ctx, 'You need to give the response number to get the details')
        elif rnum <= 0:
            await error_embed(ctx, 'You need to give a **positive non zero** response number')
        else:
            with open('./data/responses.json') as jsonResp:
                response_list = json.load(jsonResp)
                try:
                    await help_embed(ctx, f'Response #{rnum} details:', (response_list[rnum - 1]['regex']), (response_list[rnum - 1]['description']), (response_list[rnum - 1]['title']))
                except IndexError:
                    await error_embed(ctx, 'There is no response with that number yet')

    @response.command()
    @commands.check(mod_group)
    async def remove(self, ctx, rnum: int = None):
        if rnum is None:
            await error_embed(ctx, 'You need to give the response number to remove it')
        elif rnum <= 0:
            await error_embed(ctx, 'You need to give a **positive non zero** response number')
        else:
            with open('./data/responses.json') as jsonResp:
                response_list = json.load(jsonResp)
            if rnum <= len(response_list):
                frep = []
                for x in range(1, (len(response_list)+1)):
                    if x != rnum:
                        frep.append(response_list[x - 1])
                with open('./data/responses.json', 'w') as file:
                    json.dump(frep, file, indent=2)
                await channel_embed(ctx, f'Removed response #{rnum}:', (response_list[rnum - 1]["title"]))
                logging.info(f'{ctx.author.id} removed response #{rnum}, \"{(response_list[rnum - 1]["title"])}\"')
            else:
                await error_embed(ctx, 'There is no response with that number')

    @response.command()
    @commands.check(mod_group)
    async def add(self, ctx, eregex=None, etitle=None, *, edesc=None):
        if eregex is None:
            await error_embed(ctx, 'You need to give a regex')
        if etitle is None:
            await error_embed(ctx, 'You need to give a title')
        elif edesc is None:
            await error_embed(ctx, 'You need to give a description')
        else:  # maybe add a try and see if the regex valid (dont know if i can verify)
            with open('./data/responses.json') as jsonValues:
                response_list = json.load(jsonValues)
            response_list.append({'regex': eregex, 'title': etitle, 'description': edesc})
            with open('./data/responses.json', 'w') as file:
                json.dump(response_list, file, indent=2)
            await help_embed(ctx, 'New response:', eregex, edesc, etitle)
            logging.info(f'{ctx.author.id} added response with title: {etitle}')

    @response.error
    @list.error
    @details.error
    @add.error
    @remove.error
    async def response_error(self, ctx, error):
        if isinstance(error, commands.errors.BadArgument):
            await error_embed(ctx, 'You need to give the response **number** to remove/get the details of it')
        elif not isinstance(error, commands.errors.CheckFailure):
            await error_embed(ctx, None, error), await console(ctx, error)


def setup(bot):
    bot.add_cog(Response(bot))
