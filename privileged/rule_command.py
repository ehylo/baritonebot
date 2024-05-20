import discord
from discord.ext import commands

from utils import slash_embed


class Rule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(description='show a specific rule')
    @discord.app_commands.describe(rule_num='the specific rule you want')
    @discord.app_commands.rename(rule_num='rule-number')
    async def rule(self, inter: discord.Interaction, rule_num: discord.app_commands.Range[int, 1],):
        rules = list(self.bot.db.get_rules(inter.guild.id).values())

        # make sure the given rule number is in the correct bounds
        if len(rules) < rule_num:
            return await slash_embed(inter, inter.user, f'There are only {len(rules)} rules not {rule_num}!')

        await slash_embed(
            inter,
            inter.user,
            rules[rule_num - 1]['description'],
            rules[rule_num - 1]['title'],
            self.bot.db.get_embed_color(inter.guild.id),
            False
        )


async def setup(bot):
    await bot.add_cog(Rule(bot))
