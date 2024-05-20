import discord
from discord.ext import commands

from utils import info_embed


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name='user-info', description='shows information about a member/user')
    @discord.app_commands.describe(user='the user to get information on')
    async def user_info(self, inter: discord.Interaction, user: discord.User):
        await inter.response.send_message(embed=info_embed(self.bot.db, inter, user))

    @discord.app_commands.command(name='server-info', description='shows information about the server')
    async def server_info(self, inter: discord.Interaction):

        # build the embed with information about the server
        embed_var = discord.Embed(
            color=self.bot.db.get_embed_color(inter.guild.id), title=f'Server Information: {inter.guild.name}'
        )
        embed_var.add_field(name='Owner:', value=f'{inter.guild.owner} (ID: {inter.guild.owner_id})', inline=False)
        embed_var.add_field(name='Description:', value=inter.guild.description, inline=False)
        embed_var.add_field(
            name='Created:',
            value=inter.guild.created_at.strftime('%B %d, %Y at %I:%M:%S %p').lstrip('0').replace(' 0', ' '),
            inline=False
        )
        embed_var.add_field(name='Server Boosts:', value=inter.guild.premium_subscription_count, inline=False)
        embed_var.add_field(
            name=f'Roles ({len(inter.guild.roles)-1}):',
            value=(' '.join([str(r.mention) for r in inter.guild.roles][1:])+'\u200b'),
            inline=False
        )
        embed_var.add_field(name='Text Channels:', value=str(len(inter.guild.text_channels)))
        embed_var.add_field(name='Voice Channels:', value=str(len(inter.guild.voice_channels)))
        embed_var.add_field(name='Members:', value=inter.guild.member_count)

        embed_var.set_thumbnail(url=inter.guild.icon.url)
        embed_var.set_footer(text=f'{inter.user.name} | ID: {inter.user.id}', icon_url=inter.user.display_avatar.url)
        await inter.response.send_message(embed=embed_var)


async def setup(bot):
    await bot.add_cog(Info(bot))
