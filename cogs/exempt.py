import discord
import main
from discord.ext import commands


class Exempt(commands.Cog):
    def __init__(self, bot):
        """Returns embeds and inserts ids into the db for exempt related commands."""
        self.bot = bot

    @commands.group(invoke_without_command=True, case_insensitive=True, aliases=['ex'])
    @commands.check(main.admin_group)
    async def exempt(self, ctx, channel: discord.TextChannel = None):
        if channel is None:
            if ctx.guild is not None:
                channel = ctx.channel
            else:
                return await main.error_embed(ctx, 'You cannot use this command in DMs')
        main.cur.execute('SELECT ids FROM exempted WHERE ids=%s', (channel.id,))
        if main.cur.fetchone() is None:
            main.cur.execute('INSERT INTO exempted(ids, type) VALUES(%s, %s)', (channel.id, 'channel'))
            main.db.commit()
            self.bot.reload_extension('cogs.event')
            await main.channel_embed(ctx, 'Exempted', f'The channel {channel.mention} is now on the exempted list')
            print(f'{ctx.author.id} added a channel ({channel.id}) on the exempted list')
        else:
            await main.error_embed(ctx, 'This channel is already on the exempted list')

    @exempt.command(aliases=['l'])
    @commands.check(main.admin_group)
    async def list(self, ctx):
        main.cur.execute("SELECT ids FROM exempted WHERE type='channel'")
        exm_channels = [str(item[0]) for item in main.cur.fetchall()]
        await main.channel_embed(ctx, f'Exempted Channels ({len(exm_channels)})', '<#'+'>, <#'.join(exm_channels)+'>')

    @commands.group(invoke_without_command=True, case_insensitive=True, aliases=['unex'])
    @commands.check(main.admin_group)
    async def unexempt(self, ctx, channel: discord.TextChannel = None):
        if channel is None:
            if ctx.guild is not None:
                channel = ctx.channel
            else:
                await main.error_embed(ctx, 'You cannot use this command in DMs')
        main.cur.execute('SELECT ids FROM exempted WHERE ids=%s', (channel.id,))
        if main.cur.fetchone() is not None:
            main.cur.execute('DELETE FROM exempted WHERE ids=%s', (channel.id,))
            main.db.commit()
            self.bot.reload_extension('cogs.event')
            await main.channel_embed(ctx, 'Un-exempted', f'The channel {channel.mention} is no longer on the exempted list')
            print(f'{ctx.author.id} removed a channel ({channel.id}) on the exempted list')
        else:
            await main.error_embed(ctx, 'This channel is not on the exempted list')

    @unexempt.command(aliases=['l', 'list'])
    @commands.check(main.admin_group)
    async def listun(self, ctx):
        main.cur.execute("SELECT ids FROM exempted WHERE type='channel'")  # don't look at the lines below
        slist = [self.bot.get_channel(int(line)) for line in [str(item[0]) for item in main.cur.fetchall()]]
        klist = [(str(channel.id)) for channel in [x for x in self.bot.get_guild(main.ids(1)).text_channels if x not in slist]]
        await main.channel_embed(ctx, f'Unexempted Channels ({len(klist)})', f'<#{(">, <#".join(klist))}>')


def setup(bot):
    bot.add_cog(Exempt(bot))
