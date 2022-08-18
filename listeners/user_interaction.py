import discord
from discord.ext import commands

from main import bot_db
from utils.embeds import slash_embed
from utils.const import GUILD_ID
from utils.misc import info_embed


class UserInteraction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.user_command(name='member-info', guild_ids=[GUILD_ID])
    async def member_info(self, ctx, _member):
        await ctx.respond(embed=info_embed(bot_db, ctx, ctx.author))

    @discord.user_command(name='user-avatar', guild_ids=[GUILD_ID])
    async def user_avatar(self, ctx, member):
        embed_var = discord.Embed(color=bot_db.embed_color[ctx.guild.id], title='User Avatar')
        embed_var.set_image(url=member.avatar.url)
        await ctx.respond(embed=embed_var)

    @discord.user_command(name='user-banner', guild_ids=[GUILD_ID])
    async def user_banner(self, ctx, member):
        if member.banner is None:
            return await slash_embed(ctx, ctx.author, 'This user does not have a banner', 'No banner')
        embed_var = discord.Embed(color=bot_db.embed_color[ctx.guild.id], title='User Banner')
        embed_var.set_image(url=member.banner.url)
        await ctx.respond(embed=embed_var)


def setup(bot):
    bot.add_cog(UserInteraction(bot))
