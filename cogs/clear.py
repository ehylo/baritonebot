import discord
import main
from discord.ext import commands
from cogs.help import Help


class Clear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True, case_insensitive=True, aliases=['cl', 'pg', 'purge'])
    @commands.check(main.mod_group)
    async def clear(self, ctx, num=None, num2=None):
        try:
            user_men = str(ctx.message.raw_mentions[0])
        except IndexError:
            user_men = ''
        if num is None:
            await Help.clear(self, ctx)
        elif ctx.guild is None:
            await main.error_embed(ctx, 'You cannot use this command in DMs')
        else:
            if (user_men == '') and (len(num) != 18) and (num.isdigit()):  # make sure a number is given and its not an ID
                int_num = int(num)
                if int_num > 0:
                    await ctx.channel.purge(limit=int_num)
                    channel = await self.bot.fetch_channel(main.logChannel)
                    await main.log_embed(None, 'Bulk messages deleted', f'{ctx.author.mention} cleared {int_num} messages in {ctx.channel.mention}', channel, ctx.author)
                    print(f'{ctx.author.id} cleared {int_num} messages in {ctx.channel}')
                else:
                    await main.error_embed(ctx, 'You need to give a positive non zero number')
            else:
                int_num2 = int(num2)
                if int_num2 > 0:
                    limit = 0
                    if user_men != '':
                        clear_member = self.bot.get_user(int(user_men))  # get the user if they mentioned
                    elif (num.isdigit()) and (len(num) == 18):
                        clear_member = self.bot.get_user(int(num))  # get the user if they gave an ID
                    else:
                        clear_member = ctx.guild.get_member_named(num)  # get the member if they gave a name with/without discrimitor
                    if clear_member is None:
                        await main.error_embed(ctx, 'The user you gave is either invalid or the name you gave is not a member')
                    else:
                        async for message in ctx.channel.history(limit=None):
                            limit += 1
                            if message.author == clear_member:
                                int_num2 -= 1
                            if int_num2 == 0:
                                break

                        def member_check(m):
                            return m.author == clear_member

                        await ctx.channel.purge(limit=limit, check=member_check)
                        try:
                            await ctx.message.delete()  # delete the command
                        except discord.NotFound:  # ignore error if it was already deleted
                            pass
                        channel = await self.bot.fetch_channel(main.logChannel)
                        await main.log_embed(ctx, 'Bulk messages deleted', f'{ctx.author.mention} cleared {num2} messages in {ctx.channel.mention} from {clear_member.mention}', channel, clear_member)
                        print(f'{ctx.author.id} cleared {num2} messages in {ctx.channel.id} from {clear_member.id}')
                else:
                    await main.error_embed(ctx, 'You need to give a positive non zero number')


def setup(bot):
    bot.add_cog(Clear(bot))
