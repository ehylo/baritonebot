import discord
import logging
import random
from discord.ext import commands
from cogs.help import Help
from const import mod_group, channel_embed, error_embed, helper_group, fault_footer, coolEmbedColor, timeDate


class Cringe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True, case_insensitive=True, aliases=['c'])
    async def cringe(self, ctx, arg=None):
        if (arg is not None) and (arg.lower() == 'help'):
            await Help.cringe(self, ctx)
        else:
            try:
                f = open("./data/cringe.txt", "r")
                em_v = discord.Embed(color=coolEmbedColor, timestamp=timeDate, title=':camera_with_flash:')
                em_v.set_image(url=((f.readlines())[(random.randint(1, (sum(1 for _ in open("./data/cringe.txt"))))) - 1]))
                em_v.set_footer(text=fault_footer)
                await ctx.send(embed=em_v)
            except ValueError:
                await error_embed(ctx, 'There is no cringe, please add one to use this command')

    @cringe.command(aliases=['r'])
    @commands.check(mod_group)
    async def remove(self, ctx, url=None):
        if url is None:
            await error_embed(ctx, 'You need to give a url to remove')
        else:
            num_lines = sum(1 for _ in open("./data/cringe.txt"))
            tlines = 1
            f = open("./data/cringe.txt", "r")
            lines = f.readlines()
            res = [sub.replace('\n', '') for sub in lines]
            if url in res:
                with open("./data/cringe.txt", "r") as f:
                    lines = f.readlines()
                with open("./data/cringe.txt", "w") as f:
                    for line in lines:
                        tlines += 1
                        if tlines == num_lines and (line.strip("\n") == url):
                            with open("./data/cringe.txt", "r") as d:
                                llines = d.readlines()
                            with open("./data/cringe.txt", "w") as d:
                                for lline in llines:
                                    if tlines != num_lines and lline.strip("\n") != url:
                                        f.write(lline)
                                    elif tlines == num_lines:
                                        sline = lline.strip('\n')
                                        f.write(sline)
                            d.close()
                        elif tlines != num_lines and line.strip("\n") != url:
                            f.write(line)
                        elif tlines == num_lines:
                            sline = line.strip('\n')
                            f.write(sline)
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
            async def add_cringe():
                f = open("./data/cringe.txt", "r")
                lines = f.readlines()
                if len(ctx.message.attachments) > 0 or url not in [sub.replace('\n', '') for sub in lines]:
                    f = open("./data/cringe.txt", "a")
                    if len(ctx.message.attachments) > 0:
                        f.write(f'\n{ctx.message.attachments[0].url}')
                    else:
                        f.write(f'\n{url}')
                    f.close()
                    await channel_embed(ctx, 'Added', 'Very cringe')
                    logging.info(f'{ctx.author.id} added a cringe')
                else:
                    await error_embed(ctx, 'That cringe already exists')
            if len(ctx.message.attachments) > 0:
                if ctx.message.attachments[0].url.lower().endswith(('.png', '.jpeg', '.jpg', '.gif')):
                    await add_cringe()
                else:
                    await error_embed(ctx, 'Invalid attachment, must be `.png`, `.gif`, `.jpeg`, or `.jpg`')
            elif url is not None:
                if url.startswith('https://') and url.endswith(('.png', '.jpeg', '.jpg', '.gif')):
                    await add_cringe()
                else:
                    await error_embed(ctx, 'Invalid url, must be `.png`, `.gif`, `.jpeg`, or `.jpg`')


def setup(bot):
    bot.add_cog(Cringe(bot))
