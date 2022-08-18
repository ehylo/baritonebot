import discord
from discord.commands import Option
from discord.ext import commands

from main import bot_db
from utils.embeds import slash_embed
from utils.const import GUILD_ID


class Rule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name='rule', description='show a specific rule', guild_ids=[GUILD_ID])
    async def rule(
        self,
        ctx,
        rule_num: Option(
            int,
            name='rule-number',
            description='the specific rule you want',
            min=1,
            required=True
        ),
    ):
        rules_titles = bot_db.rules_titles[ctx.guild.id]
        if len(rules_titles) < rule_num:
            return await slash_embed(ctx, ctx.author, f'There are only {len(rules_titles)} rules not {rule_num}!')
        await slash_embed(
            ctx,
            ctx.author,
            bot_db.rules_descriptions[ctx.guild.id][rule_num - 1],
            rules_titles[rule_num - 1],
            bot_db.embed_color[ctx.guild.id],
            False
        )


def setup(bot):
    bot.add_cog(Rule(bot))
