import discord
from discord.ext import commands
from discord.commands import permissions, Option

from main import bot_db
from utils.embeds import slash_embed
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

        await slash_embed(ctx, ctx.author, '')
        await main.channel_embed(ctx, f'Removed response #{num}:', response[1])

    @discord.slash_command(
        name='response-list',
        description='shows a list of all the current response',
        guild_ids=[GUILD_ID],
        default_permissions=False
    )
    @permissions.has_any_role(*sum((bot_db.helper_ids | bot_db.mod_ids | bot_db.admin_ids).values(), []))
    async def response_list(self, ctx):
        description = ''
        title = bot_db.response_title[ctx.guild.id]
        regex = bot_db.response_regex[ctx.guild.id]
        for response_num in range(regex):
            description += f'**{response_num + 1}.** Title: {title[response_num]} \nRegex: `{regex[response_num]}`\n'
        # TODO: make this pages so we don't reach embed limit
        await slash_embed(
            ctx, ctx.author, description, f'Current Responses ({len(regex)}):', bot_db.embed_color[ctx.guild.id]
        )

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
        num: Option(
            int,
            name='response number',
            description='which response you want to get the details of',
            min_value=1,
            required=True
        )
    ):
        if len(bot_db.response_regex[ctx.guild.id]) < num:
            return await slash_embed(ctx, ctx.author, 'There are not that many responses', 'Bad Number')
        ignored_roles = ''
        for i in bot_db.response_ignored_roles[ctx.guild.id][num - 1].strip('}{').split(','):
            ignored_roles += f', <@&{i}>'
        regex = bot_db.response_regex[ctx.guild.id][num - 1]
        delete_message = bot_db.response_delete_message[ctx.guild.id][num - 1]
        embed_var = discord.Embed(color=bot_db.embed_color[ctx.guild.id])
        embed_var.title = f'Response #{num} details:'
        embed_var.description = f'\u2022 Regex: `{regex}` \n\u2022 Deletes message? {delete_message} \n\u2022 Ignored roles: \n{ignored_roles[2:]}'
        embed_var.add_field(
            name=bot_db.response_title[ctx.guild.id][num - 1], value=bot_db.response_description[ctx.guild.id][num - 1]
        )
        embed_var.set_footer(text=f'{ctx.author.name} | ID: {ctx.author.id}', icon_url=ctx.author.avatar.url)
        await ctx.respond(embed=embed_var)


def setup(bot):
    bot.add_cog(Response(bot))
