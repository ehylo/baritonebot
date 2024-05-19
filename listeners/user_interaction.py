import discord
from discord.ext import commands

from utils import slash_embed, info_embed


class UserInteraction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ctx_menu_1 = discord.app_commands.ContextMenu(name='member info', callback=self.member_info)
        self.ctx_menu_2 = discord.app_commands.ContextMenu(name='user avatar', callback=self.user_avatar)
        self.ctx_menu_3 = discord.app_commands.ContextMenu(name='user banner', callback=self.user_banner)
        self.bot.tree.add_command(self.ctx_menu_1)
        self.bot.tree.add_command(self.ctx_menu_2)
        self.bot.tree.add_command(self.ctx_menu_3)

    async def cog_unload(self):
        self.bot.tree.remove_command(self.ctx_menu_1.name, type=self.ctx_menu_1.type)
        self.bot.tree.remove_command(self.ctx_menu_2.name, type=self.ctx_menu_2.type)
        self.bot.tree.remove_command(self.ctx_menu_3.name, type=self.ctx_menu_3.type)

    async def member_info(self, inter: discord.Interaction, member: discord.User):
        await inter.response.send_message(embed=info_embed(self.bot.db, inter, member))

    async def user_avatar(self, inter: discord.Interaction, member: discord.Member):
        embed_var = discord.Embed(color=self.bot.db.get_embed_color(inter.guild.id), title='User Avatar')
        embed_var.set_image(url=member.display_avatar.url)
        await inter.response.send_message(embed=embed_var)

    async def user_banner(self, inter: discord.Interaction, member: discord.Member):
        if member.banner is None:
            return await slash_embed(inter, inter.user, 'This user does not have a banner', 'No banner')
        embed_var = discord.Embed(color=self.bot.db.get_embed_color(inter.guild.id), title='User Banner')
        embed_var.set_image(url=member.banner.url)
        await inter.response.send_message(embed=embed_var)


async def setup(bot):
    await bot.add_cog(UserInteraction(bot))
