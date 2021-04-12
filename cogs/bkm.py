import discord
import logging
from cogs.help import Help
from discord.ext import commands
from cogs.const import helper_group, mod_group, admin_group, muteRole, channel_embed, log_embed, error_embed, help_embed, logChannel

class Bkm(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.check(admin_group)
    async def unban(self, ctx, userId=None):
        if userId == None:
            await Help.unban(self, ctx)
        else:
            try:
                user = await self.bot.fetch_user(userId)
                try:
                    await ctx.guild.unban(user)
                    title = 'User Unbanned'
                    desc = (f'{user.name}#{user.discriminator} has been unbanned!')
                    await channel_embed(ctx, title, desc)
                    channel = await self.bot.fetch_channel(logChannel)
                    await log_embed(ctx, title, desc, channel)
                    logging.info(f'{ctx.author.id} unbanned {user.id}')
                except:
                    desc = 'That user is not banned'
                    await error_embed(ctx, desc)
            except:
                desc = 'The ID you gave is not valid'
                await error_embed(ctx, desc)

    @commands.command()
    @commands.check(mod_group)
    async def unmute(self, ctx, member: discord.Member=None):
        roleVar = discord.utils.get(ctx.guild.roles, id=muteRole)
        if member == None:
            await Help.unmute(self, ctx)
        elif member.top_role == ctx.author.top_role:
            desc = (f'You don\'t outrank {member.mention}')
            await error_embed(ctx, desc)
        else:
            channel = await self.bot.fetch_channel(logChannel)
            desc = f'{member.mention} has been unmuted'
            title = 'User Unmuted'
            await channel_embed(ctx, title, desc)
            await log_embed(ctx, title, desc, channel)
            logging.info(f'{ctx.author.id} unmuted {member.id}')
            await member.remove_roles(roleVar)

    @commands.command()
    @commands.check(mod_group)
    async def ban(self, ctx, member: discord.Member=None, *, reason=None):
        if member == None:
            await Help.ban(self, ctx)
        elif member.top_role == ctx.author.top_role:
            desc = (f'You don\'t outrank {member.mention}')
            await error_embed(ctx, desc)
        else: 
            if reason == None:
                desc = ('You need to give a reason')
                await error_embed(ctx, desc)
            else:
                await member.ban(reason=reason)
                desc = f'{member.mention} has been banned for reason: \n```{reason}```'
                title = 'User Banned'
                channel = await self.bot.fetch_channel(logChannel)
                await channel_embed(ctx, title, desc)
                await log_embed(ctx, title, desc, channel)
                logging.info(f'{ctx.author.id} banned {member.id} for reason: {reason}')


    @commands.command()
    @commands.check(helper_group)
    async def mute(self, ctx, member: discord.Member=None, *, reason=None):
        roleVar = discord.utils.get(ctx.guild.roles, id=muteRole)
        if member == None:
            await Help.mute(self, ctx)
        elif member.top_role == ctx.author.top_role:
            desc = (f'You don\'t outrank {member.mention}')
            await error_embed(ctx, desc)
        else: 
            if reason == None:
                desc = ('You need to give a reason')
                await error_embed(ctx, desc)
            else:
                desc = f'{member.mention} has been muted for reason: \n```{reason}```'
                title = 'User Muted'
                await channel_embed(ctx, title, desc)
                channel = await self.bot.fetch_channel(logChannel)
                await log_embed(ctx, title, desc, channel)
                logging.info(f'{ctx.author.id} muted {member.id} for reason: {reason}')
                await member.add_roles(roleVar)

    @commands.command()
    @commands.check(mod_group)
    async def kick(self, ctx, member: discord.Member=None, *, reason=None):
        if member == None:
            await Help.kick(self, ctx)
        elif member.top_role == ctx.author.top_role:
            desc = (f'You don\'t outrank {member.mention}')
            await error_embed(ctx, desc)
        else: 
            if reason == None:
                desc = 'You need to give a reason'
                await error_embed(ctx, desc)
            else:
                desc = f'{member.mention} has been kicked for reason: \n```{reason}```'
                title = 'User Kicked'
                await channel_embed(ctx, title, desc)
                channel = await self.bot.fetch_channel(logChannel)
                await log_embed(ctx, title, desc, channel)
                logging.info(f'{ctx.author.id} kicked {member.id} for reason: {reason}')
                await member.kick(reason=reason)

    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.errors.CheckFailure):
            desc = (f'You need to be an Admin to use the command `{ctx.command}`')
            await error_embed(ctx, desc)
        else:
            desc = None
            await error_embed(ctx, desc, error)
            logging.info(f'{ctx.author.id} tried to unban but it gave the error: {error}')

    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.errors.CheckFailure):
            desc = (f'You need to be a Helper to use the command `{ctx.command}`')
            await error_embed(ctx, desc)
        elif isinstance(error, commands.errors.MemberNotFound):
            desc = f'That member is invalid'
            await error_embed(ctx, desc)
        else:
            desc = None
            await error_embed(ctx, desc, error)
            logging.info(f'{ctx.author.id} tried to mute but it gave the error: {error}')

    @ban.error
    @unmute.error
    @kick.error
    async def mod_error(self, ctx, error):
        if isinstance(error, commands.errors.CheckFailure):
            desc = (f'You need to be a Moderator to use the command `{ctx.command}`')
            await error_embed(ctx, desc)
        elif isinstance(error, commands.errors.MemberNotFound):
            desc = f'That member is invalid'
            await error_embed(ctx, desc)
        else:
            desc = None
            await error_embed(ctx, desc, error)
            logging.info(f'{ctx.author.id} tried to ban/kick/unmute but it gave the error: {error}')

def setup(bot):
    bot.add_cog(Bkm(bot))