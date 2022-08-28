import requests

import discord
from discord.ext import commands
from discord.commands import Option

from utils.const import GUILD_ID, PASTE_TOKEN
from utils.embeds import slash_embed
from utils.misc import get_random_cringe
from main import bot_db


class ReCringe(discord.ui.View):
    @discord.ui.button(label='New Cringe', emoji='🔄', style=discord.ButtonStyle.blurple, custom_id='new_cringe')
    async def button_callback(self, _button, inter):
        embed_var = discord.Embed(color=bot_db.embed_color[inter.guild.id], title=':camera_with_flash:')
        embed_var.set_image(url=get_random_cringe(bot_db, inter))
        embed_var.set_footer(text=f'{inter.user.name} | ID: {inter.user.id}', icon_url=inter.user.display_avatar.url)
        await inter.response.edit_message(embed=embed_var, view=self)


class Cringe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(ReCringe(timeout=None))

    @discord.slash_command(name='cringe', description='retrieve a cringe image from the DB', guild_ids=[GUILD_ID])
    async def cringe(self, ctx):
        embed_var = discord.Embed(color=bot_db.embed_color[ctx.guild.id], title=':camera_with_flash:')
        embed_var.set_image(url=get_random_cringe(bot_db, ctx))
        embed_var.set_footer(text=f'{ctx.author.name} | ID: {ctx.author.id}', icon_url=ctx.author.display_avatar.url)
        await ctx.respond(embed=embed_var, view=ReCringe(timeout=None))

    @discord.slash_command(
        name='cringe-dump',
        description='dumps all cringe images into a paste.ee link',
        guild_ids=[GUILD_ID]
    )
    async def cringe_dump(self, ctx):
        paste = requests.post(
            url='https://api.paste.ee/v1/pastes',
            json={
                'sections': [{
                        'name': ctx.guild.name + ' Cringe List',
                        'contents': str('\n'.join(bot_db.cringe_list[ctx.guild.id]))
                    }]
            },
            headers={'X-Auth-Token': PASTE_TOKEN}
        ).json()
        await slash_embed(
            ctx,
            ctx.author,
            'Cringe urls available here: ' + paste['link'],
            'Cringe Dump',
            bot_db.embed_color[ctx.guild.id],
            False
        )

    @discord.slash_command(
        name='cringe-remove',
        description='remove a specific cringe image from the DB',
        guild_ids=[GUILD_ID]
    )
    @discord.default_permissions(ban_members=True)
    async def cringe_remove(
        self,
        ctx,
        url: Option(name='link', description='link to remove from the DB', required=True)
    ):
        cringe_list = bot_db.cringe_list[ctx.guild.id]
        if url in cringe_list:
            cringe_list.remove(url)
            bot_db.update_cringe_list(ctx.guild, cringe_list)
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
        guild_ids=[GUILD_ID]
    )
    @discord.default_permissions(view_audit_log=True)
    async def cringe_add(
        self,
        ctx,
        image: Option(discord.Attachment, name='image', description='image to add to the DB', required=True)
    ):
        if 'image/' not in image.content_type:
            return await slash_embed(ctx, ctx.author, 'That attachment is not an image', 'Not an Image')
        c_list = bot_db.cringe_list[ctx.guild.id]
        c_list.append(image.url)
        bot_db.update_cringe_list(ctx.guild, c_list)
        await slash_embed(ctx, ctx.author, 'Very Cringe', 'Added', bot_db.embed_color[ctx.guild.id], False)


def setup(bot):
    bot.add_cog(Cringe(bot))
