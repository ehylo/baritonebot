import discord
import json
import os
import sys
import logging
from cogs.help import Help
from discord.ext import commands
from cogs.const import channel_embed, error_embed, fault_footer, coolEmbedColor, timeDate

class Rule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def rule(self, ctx, rulenum: int=None):
        if rulenum == None:
            await Help.rule(self, ctx)
        else:
            with open(os.path.join(sys.path[0], 'data/rules.json')) as jsonRules:
                rulesStr = json.load(jsonRules)
                try:
                    sendRule = (rulesStr)[0][f'{rulenum}']
                    desc = ((sendRule)['desc'])
                    title = ((sendRule)['title'])
                    await channel_embed(ctx, title, desc)
                except:
                    desc = ('That rule does not exist yet')
                    await error_embed(ctx, desc)

    @commands.command()
    async def rules(self, ctx):
        with open(os.path.join(sys.path[0], 'data/rules.json')) as jsonRules:
                rulesStr = json.load(jsonRules)
        embedVar = discord.Embed(color = coolEmbedColor, timestamp=timeDate)
        embedVar.title = 'Rules'
        embedVar.set_footer(text=(fault_footer))
        embedVar.set_thumbnail(url='https://bigrat.monster/media/noanime.gif')
        for x in range (1, 7):
            fieldName = (((rulesStr)[0][f'{x}'])['title'])
            fieldValue = (((rulesStr)[0][f'{x}'])['desc'])
            embedVar.add_field(name=fieldName, value=fieldValue, inline=False)
        await ctx.send(embed=embedVar)

    @rule.error
    @rules.error
    async def rule_error(self, ctx, error):
        if isinstance(error, commands.errors.BadArgument):
            desc = ('You need to give a rule **number**')
            await error_embed(ctx, desc)
        else:
            desc = None
            await error_embed(ctx, desc, error)
            logging.info(f'{ctx.author.id} tried to get a rule but it gave the error: {error}')

def setup(bot):
    bot.add_cog(Rule(bot))