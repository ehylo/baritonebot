import discord
import datetime
from discord.ext import commands
from cogs.help import Help
from const import baritoneDiscord, coolEmbedColor, error_embed


async def info_embed(ctx, member, title, field1, field2, field3, value):
    em_v = discord.Embed(color=coolEmbedColor, timestamp=datetime.datetime.utcnow(), title=title)
    em_v.add_field(name='Mention:', value=member.mention, inline=True)
    em_v.add_field(name='Status:', value=field1, inline=True)
    em_v.add_field(name='Created:', value=member.created_at.strftime("%B %d, %Y at %I:%M:%S %p").lstrip("0").replace(" 0", " "), inline=False)
    em_v.add_field(name='Joined:', value=field2, inline=False)
    em_v.add_field(name=field3, value=value, inline=False)
    em_v.set_author(name=f'{member.name}#{member.discriminator}', icon_url=member.avatar_url)
    em_v.set_footer(text=f'ID: {member.id}')
    em_v.set_thumbnail(url=member.avatar_url)
    await ctx.send(embed=em_v)


async def varistuff(ctx, member, ismember):
    if ismember is True:
        await info_embed(ctx, member, 'Member Information:', member.status, member.joined_at.strftime("%B %d, %Y at %I:%M:%S %p").lstrip("0").replace(" 0", " "), f'Roles ({len(member.roles)-1}):', (' '.join([str(r.mention) for r in member.roles][1:])+'\u200b'))
    elif ismember is False:
        await info_embed(ctx, member, 'User Information:', 'API doesn\'t support this yet', 'User has not joined the baritone server yet', 'Default avatar color:', member.default_avatar)


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True, case_insensitive=True, aliases=['ui'])
    async def userinfo(self, ctx, user_id=None):
        user_men = str(ctx.message.raw_mentions)[1:-1]
        if user_id is None:
            await Help.userinfo(self, ctx)
        else:
            if user_men != '':
                clear_member = await self.bot.fetch_user(int(user_men))  # get the user if they mentioned
            elif (user_id.isdigit()) and (len(user_id) == 18):
                clear_member = await self.bot.fetch_user(int(user_id))  # get the user if they gave an ID
            else:
                clear_member = ctx.guild.get_member_named(user_id)  # get the member if they gave a name with/without discrimitor
            if clear_member is None:
                await error_embed(ctx, 'The user you gave is invalid')
            else:
                if ctx.guild.get_member(clear_member.id) is not None:
                    member = ctx.guild.get_member(clear_member.id)
                    await varistuff(ctx, member, ismember=True)
                else:
                    member = await self.bot.fetch_user(clear_member.id)
                    await varistuff(ctx, member, ismember=False)

    @userinfo.command()
    async def me(self, ctx):
        b_guild = self.bot.get_guild(baritoneDiscord)
        member_check = b_guild.get_member(ctx.author.id)
        if member_check is not None:
            await varistuff(ctx, member_check, ismember=True)
        else:
            await varistuff(ctx, ctx.author, ismember=False)

    @commands.command(aliases=['si'])
    async def serverinfo(self, ctx, arg=None):
        if (arg is not None) and (arg.lower() == 'help'):
            await Help.serverinfo(self, ctx)
        else:
            b_guild = self.bot.get_guild(baritoneDiscord)
            em_v = discord.Embed(color=coolEmbedColor, timestamp=datetime.datetime.utcnow(), title=f'Server Information: {b_guild.name}')
            em_v.add_field(name='Owner:', value=f'{b_guild.owner} (ID: {b_guild.owner_id})', inline=False)
            em_v.add_field(name='Description:', value=b_guild.description, inline=False)
            em_v.add_field(name='Created:', value=b_guild.created_at.strftime("%B %d, %Y at %I:%M:%S %p").lstrip("0").replace(" 0", " "), inline=False)
            em_v.add_field(name='Region:', value=b_guild.region, inline=False)
            em_v.add_field(name=f'Roles ({len(b_guild.roles)}):', value=(' '.join([str(r.mention) for r in b_guild.roles][1:])+'\u200b'), inline=False)
            em_v.add_field(name='Text Channels:', value=str(len(b_guild.text_channels)), inline=True)
            em_v.add_field(name='Voice Channels:', value=str(len(b_guild.voice_channels)), inline=True)
            em_v.add_field(name='Members:', value=b_guild.member_count, inline=True)
            em_v.set_footer(text=f'ID: {b_guild.id}')
            em_v.set_thumbnail(url=b_guild.icon_url)
            await ctx.send(embed=em_v)


def setup(bot):
    bot.add_cog(Info(bot))
