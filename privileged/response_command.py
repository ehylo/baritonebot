# TODO all commands and test

import discord
from discord.ext import commands
from discord.commands import permissions, Option

from main import bot_db
from utils.const import GUILD_ID


class Response(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(
        name='response-new', description='create a new response', guild_ids=[GUILD_ID], default_permissions=False
    )
    @permissions.has_any_role(*sum((bot_db.mod_ids | bot_db.admin_ids).values(), []))
    async def response_new(
        self,
        ctx,
        title: Option(str, name='title', description='the title for the new response', required=True),
        description: Option(str, name='description', description='the description for the new response', required=True),
        regex: Option(str, name='regex', description='the regex this response should try to match with', required=True),
        delete: Option(
            bool,
            name='delete message',
            description='should this response delete the message if the regex matches',
            required=True
        ),
        ignored_roles: Option(
            discord.Role,
            name='ignored roles',
            description='roles to be exempt from this response',
            required=True
        )
    ):
        pass

    @discord.slash_command(
        name='response-edit', description='edit a response', guild_ids=[GUILD_ID], default_permissions=False
    )
    @permissions.has_any_role(*sum((bot_db.mod_ids | bot_db.admin_ids).values(), []))
    async def response_edit(
        self,
        ctx,
        response_num: Option(
            int,
            name='response number',
            description='which response you want to edit',
            min_value=1,
            required=True
        )
    ):
        pass

    @discord.slash_command(
        name='response-delete', description='delete a response', guild_ids=[GUILD_ID], default_permissions=False
    )
    @permissions.has_any_role(*sum((bot_db.mod_ids | bot_db.admin_ids).values(), []))
    async def response_delete(
        self,
        ctx,
        response_num: Option(
            int,
            name='response number',
            description='which response you want to delete',
            min_value=1,
            required=True
        )
    ):
        pass

    @discord.slash_command(
        name='response-list',
        description='shows a list of all the current response',
        guild_ids=[GUILD_ID],
        default_permissions=False
    )
    @permissions.has_any_role(*sum((bot_db.helper_ids | bot_db.mod_ids | bot_db.admin_ids).values(), []))
    async def response_list(self, ctx):
        pass

    @discord.slash_command(
        name='response-details',
        description='shows details of a specific response',
        guild_ids=[GUILD_ID],
        default_permissions=False
    )
    @permissions.has_any_role(*sum((bot_db.helper_ids | bot_db.mod_ids | bot_db.admin_ids).values(), []))
    async def response_details(
        self,
        ctx,
        response_num: Option(
            int,
            name='response number',
            description='which response you want to get the details of',
            min_value=1,
            required=True
        )
    ):
        pass


def setup(bot):
    bot.add_cog(Response(bot))
