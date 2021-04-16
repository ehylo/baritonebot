import discord
import json
import logging
from cogs.help import Help
from discord.ext import commands
from const import channel_embed, error_embed, fault_footer, coolEmbedColor, timeDate, admin_group, help_embed


class Rule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def rule(self, ctx, rulenum: int = None):
        if rulenum is None:
            await Help.rule(self, ctx)
        elif rulenum <= 0:
            await error_embed(ctx, 'You need to give a **positive non zero** rule number')
        else:
            with open('./data/rules.json') as jsonRules:
                rules_list = json.load(jsonRules)
                try:
                    await channel_embed(ctx, (rules_list[rulenum - 1]['title']), (rules_list[rulenum - 1]['description']))
                except IndexError:
                    await error_embed(ctx, 'That rule does not exist yet')

    @rule.command()
    @commands.check(admin_group)
    async def remove(self, ctx, num: int = None):
        if num is None:
            await error_embed(ctx, 'You need to give a rule number to remove')
        elif num <= 0:
            await error_embed(ctx, 'You need to give a **positive non zero** rule number')
        else:
            with open('./data/rules.json') as jsonRules:
                rules_list = json.load(jsonRules)
            if num <= len(rules_list):
                frul = []
                for x in range(1, (len(rules_list)+1)):
                    if x != num:
                        frul.append(rules_list[x - 1])
                with open('./data/rules.json', 'w') as file:
                    json.dump(frul, file, indent=2)
                await channel_embed(ctx, f'Removed rule #{num}:', (rules_list[num - 1]["title"]))
                logging.info(f'{ctx.author.id} removed rule #{num}, \"{(rules_list[num - 1]["title"])}\"')
            else:
                await error_embed(ctx, 'There is no rule with that number')

    @rule.command()
    @commands.check(admin_group)
    async def add(self, ctx, dtitle=None, *, ddesc=None):
        if dtitle is None:
            await error_embed(ctx, 'You need to give a title')
        elif ddesc is None:
            await error_embed(ctx, 'You need to give a description')
        else:
            with open('./data/rules.json') as jsonValues:
                rules_list = json.load(jsonValues)
            rules_list.append({'title': dtitle, 'description': ddesc})
            with open('./data/rules.json', 'w') as file:
                json.dump(rules_list, file, indent=2)
            await help_embed(ctx, 'New rule:', '', ddesc, dtitle)
            logging.info(f'{ctx.author.id} added rule with title: {dtitle}')

    @commands.command()
    async def rules(self, ctx):
        with open('./data/rules.json') as jsonRules:
            rules_list = json.load(jsonRules)
        r_list = (len(rules_list) + 1)
        em_v = discord.Embed(color=coolEmbedColor, timestamp=timeDate, title='Rules')
        em_v.set_footer(text=fault_footer)
        em_v.set_thumbnail(url='https://bigrat.monster/media/noanime.gif')
        for x in range(1, r_list):
            field_title = (rules_list[x - 1]['title'])
            field_value = (rules_list[x - 1]['description'])
            em_v.add_field(name=field_title, value=field_value, inline=False)
        await ctx.send(embed=em_v)


def setup(bot):
    bot.add_cog(Rule(bot))
