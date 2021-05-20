import discord
import main
from cogs.help import Help
from discord.ext import commands


async def exempt_db(self, ctx, item, words, words2):
    main.cur.execute('SELECT ids FROM exempted WHERE ids=%s', (item.id,))
    if main.cur.fetchone() is None:
        main.cur.execute('INSERT INTO exempted(ids, type) VALUES(%s, %s)', (item.id, words))
        main.db.commit()
        self.bot.reload_extension('cogs.event')
        await main.channel_embed(ctx, 'Exempted', f'The {words} {item.mention} is now on the {words2}')
        print(f'{ctx.author.id} added a {words} ({item.id}) on the {words2}')
    else:
        await main.error_embed(ctx, f'This {words} is already on the {words2}')


async def unexempt_db(self, ctx, item, words, words2):
    main.cur.execute('SELECT ids FROM exempted WHERE ids=%s', (item.id,))
    if main.cur.fetchone() is not None:
        main.cur.execute('DELETE FROM exempted WHERE ids=%s', (item.id,))
        main.db.commit()
        self.bot.reload_extension('cogs.event')
        await main.channel_embed(ctx, 'Un-exempted', f'The {words} {item.mention} is no longer on the {words2}')
        print(f'{ctx.author.id} removed a {words} ({item.id}) on the {words2}')
    else:
        await main.error_embed(ctx, f'This {words} is not on the {words2}')


class Exempt(commands.Cog):
    def __init__(self, bot):
        """Returns embeds and inserts ids into the db for exempt related commands."""
        self.bot = bot

    @commands.group(invoke_without_command=True, case_insensitive=True, aliases=['ex'])
    @commands.check(main.admin_group)
    async def exempt(self, ctx):
        await Help.exempt(self, ctx)

    @exempt.command(aliases=['c'])
    @commands.check(main.admin_group)
    async def channel(self, ctx, channel: discord.TextChannel = None):
        if channel is None:
            if ctx.guild is not None:
                channel = ctx.channel
            else:
                await main.error_embed(ctx, 'You cannot use this command in DMs')
        await exempt_db(self, ctx, channel, 'channel', 'exempted list')

    @exempt.command(aliases=['u'])
    @commands.check(main.admin_group)
    async def user(self, ctx, user: discord.User = None):
        if user is None:
            user = ctx.author
        await exempt_db(self, ctx, user, 'user', 'DM blacklist')

    @exempt.command(aliases=['l'])
    @commands.check(main.admin_group)
    async def list(self, ctx, arg=None):
        if arg is None:
            await Help.exempt(self, ctx)
        elif arg.lower() in ['channel', 'c']:
            main.cur.execute("SELECT ids FROM exempted WHERE type='channel'")
            exm_channels = [str(item[0]) for item in main.cur.fetchall()]
            await main.channel_embed(ctx, f'Exempted Channels ({len(exm_channels)})', '<#'+'>, <#'.join(exm_channels)+'>')
        elif arg.lower() in ['user', 'u']:
            main.cur.execute("SELECT ids FROM exempted WHERE type='user'")
            exm_users = [str(item[0]) for item in main.cur.fetchall()]
            await main.channel_embed(ctx, f'Exempted Users ({len(exm_users)})', '<@'+'>, <@'.join(exm_users)+'>')

    @commands.group(invoke_without_command=True, case_insensitive=True, aliases=['unex'])
    @commands.check(main.admin_group)
    async def unexempt(self, ctx):
        await Help.exempt(self, ctx)

    @unexempt.command(aliases=['c', 'channel'])
    @commands.check(main.admin_group)
    async def channelun(self, ctx, channel: discord.TextChannel = None):
        if channel is None:
            if ctx.guild is not None:
                channel = ctx.channel
            else:
                await main.error_embed(ctx, 'You cannot use this command in DMs')
        await unexempt_db(self, ctx, channel, 'channel', 'exempted list')

    @unexempt.command(aliases=['u', 'user'])
    @commands.check(main.admin_group)
    async def userun(self, ctx, user: discord.User = None):
        if user is None:
            user = ctx.author
        await unexempt_db(self, ctx, user, 'user', 'DM blacklist')

    @unexempt.command(aliases=['l', 'list'])
    @commands.check(main.admin_group)
    async def listun(self, ctx):
        main.cur.execute("SELECT ids FROM exempted WHERE type='channel'")  # don't look at the lines below
        slist = [self.bot.get_channel(int(line)) for line in [str(item[0]) for item in main.cur.fetchall()]]
        klist = [(str(channel.id)) for channel in [x for x in self.bot.get_guild(main.ids(1)).text_channels if x not in slist]]
        await main.channel_embed(ctx, f'Unexempted Channels ({len(klist)})', f'<#{(">, <#".join(klist))}>')


def setup(bot):
    bot.add_cog(Exempt(bot))
