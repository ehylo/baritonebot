import discord
from discord.ext import commands

from utils.embeds import slash_embed


class Rule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(description='show a specific rule')
    @discord.app_commands.describe(rule_num='the specific rule you want')
    @discord.app_commands.rename(rule_num='rule-number')
    async def rule(self, inter: discord.Interaction, rule_num: discord.app_commands.Range[int, 1],):
        rules_titles = self.bot.db.rules_titles[inter.guild.id]
        if len(rules_titles) < rule_num:
            return await slash_embed(inter, inter.user, f'There are only {len(rules_titles)} rules not {rule_num}!')
        await slash_embed(
            inter,
            inter.user,
            self.bot.db.rules_descriptions[inter.guild.id][rule_num - 1],
            rules_titles[rule_num - 1],
            self.bot.db.embed_color[inter.guild.id],
            False
        )


async def setup(bot):
    await bot.add_cog(Rule(bot))
