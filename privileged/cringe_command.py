# TODO add a button to get a new cringe, look into different randomness, cringe add, cringe dump, and test

import random
import discord
from discord.ext import commands
from discord.commands import permissions, Option

from utils.const import GUILD_ID
from utils.embeds import slash_embed
from main import bot_db


class Cringe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(
        name='cringe',
        description='retrieve a cringe image from the DB',
        guild_ids=[GUILD_ID]
    )
    async def cringe(self, ctx):
        embed_var = discord.Embed(color=bot_db.embed_color[ctx.guild.id], title=':camera_with_flash:')
        cringe_list = bot_db.cringe_list[ctx.guild.id]
        embed_var.set_image(url=cringe_list[random.randint(0, len(cringe_list.length())) - 1])
        embed_var.set_footer(text=f'{ctx.author.name} | ID: {ctx.author.id}', icon_url=ctx.author.avatar_url)
        await ctx.respond(embed=embed_var)
        # TODO: add a button to spin the random again

    @discord.slash_command(
        name='cringe-dump',
        description='dumps all cringe images into a paste.ee link',
        guild_ids=[GUILD_ID]
    )
    async def cringe_dump(self, ctx):
        pass

    @discord.slash_command(
        name='cringe-remove',
        description='remove a specific cringe image from the DB',
        guild_ids=[GUILD_ID],
        default_permissions=False
    )
    @permissions.has_any_role(*sum((bot_db.mod_ids | bot_db.admin_ids).values(), []))
    async def cringe_remove(
        self,
        ctx,
        url: Option(str, name='link', description='link to remove from the DB', required=True)
    ):
        cringe_list = bot_db.cringe_list[ctx.guild.id]
        if url in cringe_list:
            cringe_list.remove(url)
            bot_db.update_cringe_list(ctx.guild.id, cringe_list)
            await slash_embed(
                ctx,
                ctx.author,
                description='I guess that was not cringe enough',
                title='Removed',
                color=bot_db.embed_color[ctx.guild.id],
                ephemeral=False
            )
        else:
            await slash_embed(ctx, ctx.author, 'That link does not exist in the cringe db', 'Invalid link')

    @discord.slash_command(
        name='cringe-add',
        description='add a cringe image to the DB',
        guild_ids=[GUILD_ID],
        default_permissions=False
    )
    @permissions.has_any_role(*sum((bot_db.helper_ids | bot_db.mod_ids | bot_db.admin_ids).values(), []))
    async def cringe_add(
        self,
        ctx,
        image: Option(discord.Attachment, name='image', description='image to add to the DB', required=True)
    ):
        pass


def setup(bot):
    bot.add_cog(Cringe(bot))
