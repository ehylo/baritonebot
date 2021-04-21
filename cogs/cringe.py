import discord
import logging
from discord.ext import commands
from cogs.help import Help
from const import mod_group, channel_embed, error_embed, helper_group, fault_footer, coolEmbedColor, timeDate, cur, db


class Cringe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True, case_insensitive=True, aliases=['c'])
    async def cringe(self, ctx, arg=None):
        if (arg is not None) and (arg.lower() == 'help'):
            await Help.cringe(self, ctx)
        else:
            cur.execute('SELECT cringe_link FROM cringe ORDER BY RANDOM() LIMIT 1')
            em_v = discord.Embed(color=coolEmbedColor, timestamp=timeDate, title=':camera_with_flash:')
            em_v.set_image(url=str(str(cur.fetchone())[2:-3]))
            em_v.set_footer(text=fault_footer)
            await ctx.send(embed=em_v)

    @cringe.command(aliases=['r'])
    @commands.check(mod_group)
    async def remove(self, ctx, url=None):
        if url is None:
            await error_embed(ctx, 'You need to give a url to remove')
        else:
            cur.execute(f'SELECT cringe_link FROM cringe WHERE cringe_link = "{url}"')
            if cur.fetchone() is not None:
                cur.execute('DELETE FROM cringe WHERE cringe_link=?', (url,))
                db.commit()
                await channel_embed(ctx, 'Removed', 'I guess that wasn\'nt cringe enough')
                logging.info(f'{ctx.author.id} removed a cringe')
            else:
                await error_embed(ctx, 'That url does not exist in the cringe db')

    @cringe.command(aliases=['a'])
    @commands.check(helper_group)
    async def add(self, ctx, url=None):
        if len(ctx.message.attachments) == 0 and url is None:
            await error_embed(ctx, 'You need to give a url or attachment to add cringe')
        else:
            async def cringe_add(aurl):
                cur.execute(f'SELECT cringe_link FROM cringe WHERE cringe_link = "{aurl}"')
                if cur.fetchone() is None:
                    cur.execute(f'INSERT INTO cringe(cringe_link) VALUES(?)', (aurl,))
                    db.commit()
                    await channel_embed(ctx, 'Added', 'Very cringe')
                    logging.info(f'{ctx.author.id} added a cringe')
                else:
                    await error_embed(ctx, 'That cringe already exists')
            if len(ctx.message.attachments) > 0:
                if ctx.message.attachments[0].url.lower().endswith(('.png', '.jpeg', '.jpg', '.gif')):
                    await cringe_add(ctx.message.attachments[0].url)
                else:
                    await error_embed(ctx, 'Invalid attachment, must be `.png`, `.gif`, `.jpeg`, or `.jpg`')
            elif url is not None:
                if url.startswith('https://') and url.endswith(('.png', '.jpeg', '.jpg', '.gif')):
                    await cringe_add(url)
                else:
                    await error_embed(ctx, 'Invalid url, must be `.png`, `.gif`, `.jpeg`, or `.jpg`')


def setup(bot):
    bot.add_cog(Cringe(bot))
