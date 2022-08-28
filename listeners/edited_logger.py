import discord
from discord.ext import commands

from main import bot_db
from utils.misc import get_channel


class EditedMessageJump(discord.ui.View):
    def __init__(self, url):
        self.url = url
        super().__init__()
        self.add_item(discord.ui.Button(label='Jump', url=url, style=discord.ButtonStyle.grey))


class EditedLogger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_edit(self, message_before, message_after):
        if message_after.author.discriminator == '0000':
            return
        if message_after.content == '' or message_before.content == '':
            return
        if message_after.author.id == bot_db.bot_id:
            return
        if message_after.content == message_before.content:
            return
        if message_after.guild is None:
            return
        if len(message_before.content) > 1024 or len(message_after.content) > 1024:
            return
        if message_after.channel.id in bot_db.exempted_ids[message_after.guild.id]:
            return
        embed_var = discord.Embed(
            color=bot_db.embed_color[message_after.guild.id],
            description=f'**Message edited in {message_after.channel.mention}**'
        )
        embed_var.add_field(name='Before Edit:', value=message_before.content, inline=False)
        embed_var.add_field(name='After Edit:', value=message_after.content, inline=False)
        embed_var.set_footer(
            text=f'{message_after.author.name} | ID: {message_after.author.id}',
            icon_url=message_after.author.display_avatar.url
        )
        channel = await get_channel(self.bot, bot_db.logs_id[message_after.guild.id])
        await channel.send(embed=embed_var, view=EditedMessageJump(message_after.jump_url))


def setup(bot):
    bot.add_cog(EditedLogger(bot))
