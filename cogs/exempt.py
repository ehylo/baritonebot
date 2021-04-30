import logging
from cogs.help import Help
from discord.ext import commands
from const import error_embed, admin_group, channel_embed, baritoneDiscord, cur, db


class Exempt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True, case_insensitive=True, aliases=['ex'])
    @commands.check(admin_group)
    async def exempt(self, ctx, arg=None):
        if (arg is not None) and (arg.lower() == 'help'):
            await Help.exempt(self, ctx)
        elif ctx.guild is None:
            await error_embed(ctx, 'You cannot use this command in DMs')
        else:
            cur.execute('SELECT channel_id FROM ex_channels WHERE channel_id=%s', (ctx.channel.id,))
            if cur.fetchone() is None:
                cur.execute('INSERT INTO ex_channels(channel_id) VALUES(%s)', (ctx.channel.id,))
                db.commit()
                self.bot.reload_extension(f'cogs.event')
                await channel_embed(ctx, 'Exempted', f'The channel {ctx.channel.mention} is now exempted from the blacklist, regex responses, and message logging')
                logging.info(f'{ctx.author.id} added a channel ({ctx.channel.id}) to the exemptchannels')
            else:
                await error_embed(ctx, 'This channel is already on the exempt list')

    @exempt.command(aliases=['list', 'l'])
    @commands.check(admin_group)
    async def show(self, ctx):  # totally didn't make this 'show' so I didn't have to make a new class :whistle:
        cur.execute('SELECT channel_id FROM ex_channels')
        exm_channels = [str(item[0]) for item in cur.fetchall()]
        await channel_embed(ctx, f'Exempted Channels ({len(exm_channels)})', '<#'+'>, <#'.join(exm_channels)+'>')

    @commands.group(invoke_without_command=True, case_insensitive=True, aliases=['unex'])
    @commands.check(admin_group)
    async def unexempt(self, ctx, arg=None):
        if (arg is not None) and (arg.lower() == 'help'):
            await Help.exempt(self, ctx)
        elif ctx.guild is None:
            await error_embed(ctx, 'You cannot use this command in DMs')
        else:
            cur.execute('SELECT channel_id FROM ex_channels WHERE channel_id=%s', (ctx.channel.id,))
            if cur.fetchone() is not None:
                cur.execute('DELETE FROM ex_channels WHERE channel_id=%s', (ctx.channel.id,))
                db.commit()
                self.bot.reload_extension('cogs.event')
                await channel_embed(ctx, 'Un-exempted', f'The channel {ctx.channel.mention} is no longer exempted from the blacklist and regex responses')
                logging.info(f'{ctx.author.id} removed a channel ({ctx.channel.id}) from the exemptchannels')
            else:
                await error_embed(ctx, 'This channel is not exempted')

    @unexempt.command(aliases=['l'])
    @commands.check(admin_group)
    async def list(self, ctx):
        cur.execute('SELECT channel_id FROM ex_channels')  # don't look at the lines below
        slist = [self.bot.get_channel(int(line)) for line in [str(item[0]) for item in cur.fetchall()]]
        klist = [(str(channel.id)) for channel in [x for x in self.bot.get_guild(baritoneDiscord).text_channels if x not in slist]]
        await channel_embed(ctx, f'Unexempted Channels ({len(klist)})', f'<#{(">, <#".join(klist))}>')


def setup(bot):
    bot.add_cog(Exempt(bot))
