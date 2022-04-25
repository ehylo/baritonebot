# TODO complete rule command and parameters

import discord
from discord.commands import permissions, Option
from discord.ext import commands

from main import bot_db
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
            name='rule number',
            description='the specific rule you want',
            choices=[1, 2, 3, 4, 5, 6],
            required=True
        ),
        sub_rule: Option(
            str,
            name='sub-rule option',
            description='which part of the rule do you want to see',
            choices=['A', 'B', 'C', 'D', 'E', 'F'],
            required=False
        )
    ):
        pass

    @discord.slash_command(
        name='rule-edit',
        description='edit a specific rule/sub-rule',
        guild_ids=[GUILD_ID],
        default_permissions=False
    )
    @permissions.has_any_role(*sum(bot_db.admin_ids.values(), []))
    async def rule_edit(
        self,
        ctx,
        rule_num: Option(
            int,
            name='rule number',
            description='the specific rule you want to edit',
            choices=[1, 2, 3, 4, 5, 6],
            required=True
        ),
        sub_rule: Option(
            str,
            name='sub-rule option',
            description='which part of the rule do you want to edit (put \'none\' to remove the sub rule)',
            choices=['A', 'B', 'C', 'D', 'E', 'F'],
            required=True
        )
    ):
        pass

    @commands.Cog.listener()
    async def on_ready(self):
        pass


def setup(bot):
    bot.add_cog(Rule(bot))
