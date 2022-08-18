import discord
from discord.ext import commands
from discord.commands import Option

from utils.const import GUILD_ID
from main import bot_db
from utils import misc


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name='user-info', description='shows information about a member/user', guild_ids=[GUILD_ID])
    async def user_info(
        self,
        ctx,
        user: Option(discord.User, name='user', description='the user to get information on', required=True)
    ):
        await ctx.respond(embed=misc.info_embed(bot_db, ctx, user))

    @discord.slash_command(name='server-info', description='shows information about the server', guild_ids=[GUILD_ID])
    async def server_info(self, ctx):
        embed_var = discord.Embed(color=bot_db.embed_color[ctx.guild.id],  title=f'Server Information: {ctx.guild.name}')
        embed_var.add_field(name='Owner:', value=f'{ctx.guild.owner} (ID: {ctx.guild.owner_id})', inline=False)
        embed_var.add_field(name='Description:', value=ctx.guild.description, inline=False)
        embed_var.add_field(
            name='Created:',
            value=ctx.guild.created_at.strftime('%B %d, %Y at %I:%M:%S %p').lstrip('0').replace(' 0', ' '),
            inline=False
        )
        embed_var.add_field(name='Server Boosts:', value=ctx.guild.premium_subscription_count, inline=False)
        embed_var.add_field(
            name=f'Roles ({len(ctx.guild.roles)-1}):',
            value=(' '.join([str(r.mention) for r in ctx.guild.roles][1:])+'\u200b'),
            inline=False
        )
        embed_var.add_field(name='Text Channels:', value=str(len(ctx.guild.text_channels)))
        embed_var.add_field(name='Voice Channels:', value=str(len(ctx.guild.voice_channels)))
        embed_var.add_field(name='Members:', value=ctx.guild.member_count)
        embed_var.set_thumbnail(url=ctx.guild.icon.url)
        embed_var.set_footer(text=f'{ctx.author.name} | ID: {ctx.author.id}', icon_url=ctx.author.avatar.url)
        await ctx.respond(embed=embed_var)


def setup(bot):
    bot.add_cog(Info(bot))
