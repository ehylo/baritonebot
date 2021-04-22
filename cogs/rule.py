import discord
import logging
from cogs.help import Help
from discord.ext import commands
from const import channel_embed, error_embed, fault_footer, coolEmbedColor, timeDate, admin_group, help_embed, cur, db


class Rule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True, case_insensitive=True, aliases=['r'])
    async def rule(self, ctx, rulenum: int = None):
        if rulenum is None:
            await Help.rule(self, ctx)
        elif rulenum <= 0:
            await error_embed(ctx, 'You need to give a **positive non zero** rule number')
        else:
            cur.execute(f'SELECT * FROM rules WHERE rules_number = {rulenum}')
            rule = cur.fetchone()
            if rule is not None:
                await channel_embed(ctx, rule[1], rule[2])
            else:
                await error_embed(ctx, 'That rule does not exist yet')

    @rule.command(aliases=['r'])
    @commands.check(admin_group)
    async def remove(self, ctx, num: int = None):
        if num is None:
            await error_embed(ctx, 'You need to give a rule number to remove')
        elif num <= 0:
            await error_embed(ctx, 'You need to give a **positive non zero** rule number')
        else:
            cur.execute(f'SELECT rules_number, rules_title FROM rules WHERE rules_number={num}')
            rule = cur.fetchone()
            if rule is not None:
                await channel_embed(ctx, f'Removed rule #{num}:', rule[1])
                logging.info(f'{ctx.author.id} removed rule #{num}, \"{rule[1]}\"')
                cur.execute(f'DELETE FROM rules WHERE rules_number={num}')
                db.commit()
            else:
                await error_embed(ctx, 'There is no rule with that number')

    @rule.command(aliases=['a'])
    @commands.check(admin_group)
    async def add(self, ctx, anum: int = None, dtitle=None, *, ddesc=None):
        if anum is None:
            await error_embed(ctx, 'You need to give a number')
        elif anum <= 0:
            await error_embed(ctx, 'You need to give a **positive non zero** rule number')
        elif dtitle is None:
            await error_embed(ctx, 'You need to give a title')
        elif ddesc is None:
            await error_embed(ctx, 'You need to give a description')
        else:
            cur.execute(f'SELECT rules_number FROM rules WHERE rules_number={anum}')
            if cur.fetchone() is None:
                cur.execute(f'INSERT INTO rules(rules_number, rules_title, rules_description) VALUES(%s, %s, %s)', (anum, dtitle, ddesc))
                db.commit()
                await help_embed(ctx, 'New rule:', f'{ctx.author.mention} added rule {anum}', ddesc, dtitle)
                logging.info(f'{ctx.author.id} added rule with title: {dtitle}')
            else:
                await error_embed(ctx, 'That rule already exists')

    @commands.command()
    async def rules(self, ctx):
        em_v = discord.Embed(color=coolEmbedColor, timestamp=timeDate, title='Rules')
        em_v.set_footer(text=fault_footer)
        em_v.set_thumbnail(url='https://bigrat.monster/media/noanime.gif')
        cur.execute('SELECT ROW_NUMBER () OVER ( ORDER BY rules_number ) rowNum, rules_number, rules_title, rules_description FROM rules')
        db.commit()
        rules = cur.fetchall()
        for row in rules:
            field_title = f'**{row[1]} )** {row[2]}'
            field_value = row[3]
            em_v.add_field(name=field_title, value=field_value, inline=False)
        await ctx.send(embed=em_v)


def setup(bot):
    bot.add_cog(Rule(bot))
