import discord
import main
from discord.ext import commands


class Cringe(commands.Cog):
    def __init__(self, bot):
        """Returns embeds for the cringe command."""
        self.bot = bot

    @commands.group(invoke_without_command=True, case_insensitive=True, aliases=['c'])
    async def cringe(self, ctx):
        em_v = discord.Embed(color=int(main.values(1), 16), title=':camera_with_flash:')
        main.cur.execute('SELECT cringe_link FROM cringe ORDER BY RANDOM() LIMIT 1')
        em_v.set_image(url=str(str(main.cur.fetchone())[2:-3]))
        em_v.set_footer(text=f'{ctx.author.name} | ID: {ctx.author.id}', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=em_v)

    @cringe.command(aliases=['r'])
    @commands.check(main.mod_group)
    async def remove(self, ctx, url=None):
        if url is None:
            await main.error_embed(ctx, 'You need to give a url to remove')
        else:
            main.cur.execute('SELECT cringe_link FROM cringe WHERE cringe_link=%s', (url,))
            if main.cur.fetchone() is not None:
                main.cur.execute('DELETE FROM cringe WHERE cringe_link=%s', (url,))
                main.db.commit()
                await main.channel_embed(ctx, 'Removed', 'I guess that wasn\'nt cringe enough')
                print(f'{ctx.author.id} removed a cringe')
            else:
                await main.error_embed(ctx, 'That url does not exist in the cringe db')

    @cringe.command(aliases=['a'])
    @commands.check(main.helper_group)
    async def add(self, ctx, url=None):
        if len(ctx.message.attachments) == 0 and url is None:
            await main.error_embed(ctx, 'You need to give a url or attachment to add cringe')
        else:
            async def cringe_add(aurl):
                main.cur.execute('SELECT cringe_link FROM cringe WHERE cringe_link=%s', (aurl,))
                if main.cur.fetchone() is None:
                    main.cur.execute('INSERT INTO cringe(cringe_link) VALUES(%s)', (aurl,))
                    main.db.commit()
                    await main.channel_embed(ctx, 'Added', 'Very cringe')
                    print(f'{ctx.author.id} added a cringe')
                else:
                    await main.error_embed(ctx, 'That cringe already exists')
            if len(ctx.message.attachments) > 0:
                if ctx.message.attachments[0].url.lower().endswith(('.png', '.jpeg', '.jpg', '.gif')):
                    await cringe_add(ctx.message.attachments[0].url)
                else:
                    await main.error_embed(ctx, 'Invalid attachment, must be `.png`, `.gif`, `.jpeg`, or `.jpg`')
            elif url is not None:
                if url.startswith('https://') and url.endswith(('.png', '.jpeg', '.jpg', '.gif')):
                    await cringe_add(url)
                else:
                    await main.error_embed(ctx, 'Invalid url, must be `.png`, `.gif`, `.jpeg`, or `.jpg`')


def setup(bot):
    bot.add_cog(Cringe(bot))
