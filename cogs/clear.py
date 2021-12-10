import discord
import main
from discord.ext import commands
from cogs.help import Help


class Clear(commands.Cog):
    def __init__(self, bot):
        """Returns embeds for the clear command."""
        self.bot = bot

    @commands.group(invoke_without_command=True, case_insensitive=True, aliases=['cl', 'pg', 'purge'])
    @commands.check(main.mod_group)
    async def clear(self, ctx, num=None, num2=None):
        if num is None:
            return await Help.clear(self, ctx)
        if ctx.guild is None:
            return await main.error_embed(ctx, 'You cannot use this command in DMs')
        args = await main.mem_check(self, num)
        channel = await self.bot.get_channel(main.ids(3))
        if args[0]:  # A member was given
            if num2 is None:
                return await main.error_embed(ctx, 'You need to give a positive non zero number')
            if not num2.isdigit():
                return await main.error_embed(ctx, 'You need to give a positive non zero number')
            int_num2 = int(num2)
            if int_num2 < 1:
                return await main.error_embed(ctx, 'You need to give a positive non zero number')
            limit = 0
            async for message in ctx.channel.history(limit=None):
                limit += 1
                if message.author == args[1]:
                    int_num2 -= 1
                if int_num2 == 0:
                    break

            def member_check(m):
                return m.author == args[1]
            await ctx.channel.purge(limit=limit, check=member_check)
            try:
                await ctx.message.delete()  # delete the command
            except discord.NotFound:  # ignore error if it was already deleted
                pass
            print(f'{ctx.author.id} cleared {num2} messages in {ctx.channel.id} from {args[1].id}')
            return await main.log_embed(ctx, 'Bulk messages deleted', f'{ctx.author.mention} cleared {num2} messages in {ctx.channel.mention} from {args[1].mention}', channel, args[1])
        if args[2]:  # A number was given
            if int(num) > 1000000000:
                return await main.error_embed(ctx, 'The number you gave is not a valid member ID or you are trying to clear over 1 Billion messages which is not allowed')
            if int(num) < 1:
                return await main.error_embed(ctx, 'You need to give a positive non zero number')
            await ctx.channel.purge(limit=int(num))
            print(f'{ctx.author.id} cleared {num} messages in {ctx.channel.id}')
            return await main.log_embed(None, 'Bulk messages deleted', f'{ctx.author.mention} cleared {num} messages in {ctx.channel.mention}', channel, ctx.author)
        return await main.error_embed(ctx, 'That is not a member or positive non zero number')


def setup(bot):
    bot.add_cog(Clear(bot))
