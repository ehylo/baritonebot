import requests

import discord
from discord.ext import commands

from utils.const import PASTE_TOKEN
from utils.embeds import slash_embed
from utils.misc import get_random_cringe


class ReCringe(discord.ui.View):
    def __init__(self, bot, timeout: int = None):
        super().__init__(timeout=timeout)
        self.bot = bot

    @discord.ui.button(label='New Cringe', emoji='🔄', style=discord.ButtonStyle.blurple, custom_id='new_cringe')
    async def button_callback(self, inter: discord.Interaction, _button: discord.ui.Button):
        embed_var = discord.Embed(color=self.bot.db.embed_color[inter.guild.id], title=':camera_with_flash:')
        embed_var.set_image(url=get_random_cringe(self.bot.db, inter))
        embed_var.set_footer(text=f'{inter.user.name} | ID: {inter.user.id}', icon_url=inter.user.display_avatar.url)
        await inter.response.edit_message(embed=embed_var, view=self)


class Cringe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(ReCringe(bot=self.bot))

    @discord.app_commands.command(description='retrieve a cringe image from the DB')
    async def cringe(self, inter: discord.Interaction):
        embed_var = discord.Embed(color=self.bot.db.embed_color[inter.guild.id], title=':camera_with_flash:')
        embed_var.set_image(url=get_random_cringe(self.bot.db, inter))
        embed_var.set_footer(text=f'{inter.user.name} | ID: {inter.user.id}', icon_url=inter.user.display_avatar.url)
        await inter.response.send_message(embed=embed_var, view=ReCringe(bot=self.bot))

    @discord.app_commands.command(name='cringe-dump', description='dumps all cringe images into a paste.ee link')
    async def cringe_dump(self, inter: discord.Interaction):
        paste = requests.post(
            url='https://api.paste.ee/v1/pastes',
            json={
                'sections': [{
                        'name': inter.guild.name + ' Cringe List',
                        'contents': str('\n'.join(self.bot.db.cringe_list[inter.guild.id]))
                    }]
            },
            headers={'X-Auth-Token': PASTE_TOKEN}
        ).json()
        await slash_embed(
            inter,
            inter.user,
            'Cringe urls available here: ' + paste['link'],
            'Cringe Dump',
            self.bot.db.embed_color[inter.guild.id],
            False
        )

    @discord.app_commands.command(name='cringe-remove', description='remove a specific cringe image from the DB')
    @discord.app_commands.default_permissions(ban_members=True)
    @discord.app_commands.describe(url='link to remove from the DB')
    @discord.app_commands.rename(url='link')
    async def cringe_remove(self, inter: discord.Interaction, url: str):
        cringe_list = self.bot.db.cringe_list[inter.guild.id]
        if url in cringe_list:
            cringe_list.remove(url)
            self.bot.db.update_cringe_list(inter.guild, cringe_list)
            await slash_embed(
                inter,
                inter.user,
                description='I guess that was not cringe enough',
                title='Removed',
                color=self.bot.db.embed_color[inter.guild.id],
                ephemeral=False
            )
        else:
            await slash_embed(inter, inter.user, 'That link does not exist in the cringe db', 'Invalid link')

    @discord.app_commands.command(name='cringe-add', description='add a cringe image to the DB')
    @discord.app_commands.default_permissions(view_audit_log=True)
    @discord.app_commands.describe(image='image to add to the DB')
    async def cringe_add(self, inter: discord.Interaction, image: discord.Attachment):
        if 'image/' not in image.content_type:
            return await slash_embed(inter, inter.user, 'That attachment is not an image', 'Not an Image')
        c_list = self.bot.db.cringe_list[inter.guild.id]
        c_list.append(image.url)
        self.bot.db.update_cringe_list(inter.guild, c_list)
        await slash_embed(inter, inter.user, 'Very Cringe', 'Added', self.bot.db.embed_color[inter.guild.id], False)


async def setup(bot):
    await bot.add_cog(Cringe(bot))
