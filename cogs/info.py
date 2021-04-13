import discord
import datetime
import logging
from discord.ext import commands
from cogs.help import Help
from cogs.const import baritoneDiscord, coolEmbedColor, error_embed

async def info_embed(ctx, member, title, field1, field2, field3, value):
    embedVar = discord.Embed(color = coolEmbedColor, timestamp=datetime.datetime.utcnow(), title=title)
    embedVar.add_field(name='Mention:', value=member.mention, inline=True)
    embedVar.add_field(name='Status:', value=field1, inline=True)
    embedVar.add_field(name='Created:', value=member.created_at.strftime("%B %d, %Y at %I:%M:%S %p").lstrip("0").replace(" 0", " "), inline=False)
    embedVar.add_field(name='Joined:', value=field2, inline=False)
    embedVar.add_field(name=field3, value=value, inline=False)
    embedVar.set_author(name=f'{member.name}#{member.discriminator}', icon_url=member.avatar_url)
    embedVar.set_footer(text=(f'ID: {member.id}'))
    embedVar.set_thumbnail(url=member.avatar_url)
    await ctx.send(embed=embedVar)

async def varistuff(ctx, member, info, ismember):
    if info == True:
        if ismember == True:
            title = 'Member Information:'
            field1 = member.status
            field2 = member.joined_at.strftime("%B %d, %Y at %I:%M:%S %p").lstrip("0").replace(" 0", " ")
            field3 = f'Roles ({len(member.roles)-1}):'
            value = (' '.join([str(r.mention) for r in member.roles][1:])+'\u200b')
            await info_embed(ctx, member, title, field1, field2, field3, value)
        elif ismember == False:
            title = 'User Information:'
            field1 = 'API doesn\'t support this yet'
            field2 = 'User has not joined this server yet'
            field3 = 'Default avatar color:'
            value = member.default_avatar
            await info_embed(ctx, member, title, field1, field2, field3, value)

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def userinfo(self, ctx, userID=None):
        usrStr = str(ctx.message.raw_mentions)[1:-1]
        memberCheck = self.bot.get_guild(baritoneDiscord)
        if userID == None:
            await Help.userinfo(self, ctx)
        else:
            if usrStr == '':
                try:
                    usrint = int(userID)
                    if memberCheck.get_member(usrint) != None:
                        member = memberCheck.get_member(usrint)
                        await varistuff(ctx, member, info=True, ismember=True)
                    elif await self.bot.fetch_user(usrint) != None: 
                        member = await self.bot.fetch_user(usrint)
                        await varistuff(ctx, member, info=True, ismember=False)
                    else:
                        desc = 'That is not a valid user ID'
                        await error_embed(ctx, desc)
                except:
                    desc = 'That isn\'t a user (needs to be a **number**)'
                    await error_embed(ctx, desc)
            else:
                usrint = int(usrStr)
                member = memberCheck.get_member(usrint)
                await varistuff(ctx, member, info=True, ismember=True)

    @userinfo.command()
    async def me(self, ctx):
        member = ctx.author
        await varistuff(ctx, member, info=True, ismember=True)

    @commands.group(invoke_without_command=True)
    async def serverinfo(self, ctx):
            embedVar = discord.Embed(color = coolEmbedColor, timestamp=datetime.datetime.utcnow(), title=f'Server Information: {ctx.guild.name}')
            embedVar.add_field(name='Owner:', value=f'{ctx.guild.owner} (ID: {ctx.guild.owner_id})', inline=False)
            embedVar.add_field(name='Description:', value=ctx.guild.description, inline=False)
            embedVar.add_field(name='Created:', value=ctx.guild.created_at.strftime("%B %d, %Y at %I:%M:%S %p").lstrip("0").replace(" 0", " "), inline=False)
            embedVar.add_field(name='Region:', value=ctx.guild.region, inline=False)
            embedVar.add_field(name=f'Roles ({len(ctx.guild.roles)}):', value=(' '.join([str(r.mention) for r in ctx.guild.roles][1:])+'\u200b'), inline=False)
            embedVar.add_field(name='Text Channels:', value=len(ctx.guild.text_channels), inline=True)
            embedVar.add_field(name='Voice Channels:', value=len(ctx.guild.voice_channels), inline=True)
            embedVar.add_field(name='Members:', value=ctx.guild.member_count, inline=True)
            embedVar.set_footer(text=(f'ID: {ctx.guild.id}'))
            embedVar.set_thumbnail(url=ctx.guild.icon_url)
            await ctx.send(embed=embedVar)

    @serverinfo.command()
    async def help(self, ctx):
        await Help.serverinfo(self, ctx)

    @serverinfo.error
    @userinfo.error
    @help.error
    async def serveruser_error(self, ctx, error):
        desc = None
        await error_embed(ctx, desc, error)
        logging.info(f'{ctx.author.id} tried to get server/user info but it gave the error: {error}')

def setup(bot):
    bot.add_cog(Info(bot))