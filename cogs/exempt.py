import main
from cogs.help import Help
from discord.ext import commands


async def help_checker(self, ctx, arg=None):
    if (arg is not None) and (arg.lower() == 'help'):
        await Help.exempt(self, ctx)
    elif ctx.guild is None:
        await main.error_embed(ctx, 'You cannot use this command in DMs')
    else:
        return True


class Exempt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True, case_insensitive=True, aliases=['ex'])
    @commands.check(main.admin_group)
    async def exempt(self, ctx, arg=None):
        if await help_checker(self, ctx, arg) is True:
            main.cur.execute('SELECT channel_id FROM ex_channels WHERE channel_id=%s', (ctx.channel.id,))
            if main.cur.fetchone() is None:
                main.cur.execute('INSERT INTO ex_channels(channel_id) VALUES(%s)', (ctx.channel.id,))
                main.db.commit()
                self.bot.reload_extension('cogs.event')
                await main.channel_embed(ctx, 'Exempted', f'The channel {ctx.channel.mention} is now exempted from the blacklist, regex responses, and message logging')
                print(f'{ctx.author.id} added a channel ({ctx.channel.id}) to the exemptchannels')
            else:
                await main.error_embed(ctx, 'This channel is already on the exempt list')

    @exempt.command(aliases=['list', 'l'])
    @commands.check(main.admin_group)
    async def show(self, ctx):  # totally didn't make this 'show' so I didn't have to make a new class :whistle:
        main.cur.execute('SELECT channel_id FROM ex_channels')
        exm_channels = [str(item[0]) for item in main.cur.fetchall()]
        await main.channel_embed(ctx, f'Exempted Channels ({len(exm_channels)})', '<#'+'>, <#'.join(exm_channels)+'>')

    @commands.group(invoke_without_command=True, case_insensitive=True, aliases=['unex'])
    @commands.check(main.admin_group)
    async def unexempt(self, ctx, arg=None):
        if await help_checker(self, ctx, arg) is True:
            main.cur.execute('SELECT channel_id FROM ex_channels WHERE channel_id=%s', (ctx.channel.id,))
            if main.cur.fetchone() is not None:
                main.cur.execute('DELETE FROM ex_channels WHERE channel_id=%s', (ctx.channel.id,))
                main.db.commit()
                self.bot.reload_extension('cogs.event')
                await main.channel_embed(ctx, 'Un-exempted', f'The channel {ctx.channel.mention} is no longer exempted from the blacklist and regex responses')
                print(f'{ctx.author.id} removed a channel ({ctx.channel.id}) from the exemptchannels')
            else:
                await main.error_embed(ctx, 'This channel is not exempted')

    @unexempt.command(aliases=['l'])
    @commands.check(main.admin_group)
    async def list(self, ctx):
        main.cur.execute('SELECT channel_id FROM ex_channels')  # don't look at the lines below
        slist = [self.bot.get_channel(int(line)) for line in [str(item[0]) for item in main.cur.fetchall()]]
        klist = [(str(channel.id)) for channel in [x for x in self.bot.get_guild(main.ids(1)).text_channels if x not in slist]]
        await main.channel_embed(ctx, f'Unexempted Channels ({len(klist)})', f'<#{(">, <#".join(klist))}>')


def setup(bot):
    bot.add_cog(Exempt(bot))
