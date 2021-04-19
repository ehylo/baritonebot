import logging

import discord
from discord.ext import commands
from cogs.help import Help
from const import logChannel, log_embed, mod_group, error_embed


class Clear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True, case_insensitive=True, aliases=['cl', 'pg', 'purge'])
    @commands.check(mod_group)
    async def clear(self, ctx, num=None, num2=None):
        user_men = str(ctx.message.raw_mentions)[1:-1]
        if num is None:
            await Help.clear(self, ctx)
        else:
            if (user_men == '') and (len(num) != 18) and (num.isdigit()):  # make sure a number is given and its not an ID
                int_num = int(num)
                if int_num > 0:
                    await ctx.channel.purge(limit=int_num)
                    channel = await self.bot.fetch_channel(logChannel)
                    await log_embed(ctx, 'Bulk messages deleted', f'{ctx.author.mention} cleared {int_num} messages in {ctx.channel.mention}', channel)
                    logging.info(f'{ctx.author.id} cleared {int_num} messages in {ctx.channel}')
                else:
                    await error_embed(ctx, 'You need to give a positive non zero number')
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
                        await error_embed(ctx, 'You need to either give an amount of messages to clear, mention someone, give an ID, or give a name')
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
                        channel = await self.bot.fetch_channel(logChannel)
                        await log_embed(ctx, 'Bulk messages deleted', f'{ctx.message.author.mention} cleared {num2} messages in {ctx.channel.mention} from {clear_member.mention}', channel)
                        logging.info(f'{ctx.author.id} cleared {num2} messages in {ctx.channel.id} from {clear_member.id}')
                else:
                    await error_embed(ctx, 'You need to give a positive non zero number')


def setup(bot):
    bot.add_cog(Clear(bot))
