import discord
import logging
import random
from discord.ext import commands
from cogs.help import Help
from const import mod_group, channel_embed, error_embed, helper_group, fault_footer, coolEmbedColor, timeDate


class Cringe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True, case_insensitive=True)
    async def cringe(self, ctx, arg=None):
        if arg == 'help':
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

    @cringe.command()
    @commands.check(mod_group)
    async def remove(self, ctx, url=None):
        if url is None:
            await error_embed(ctx, 'You need to give a url to remove')
        else:
            f = open("./data/cringe.txt", "r")
            if url in [sub.replace('\n', '') for sub in (f.readlines())]:
                with open("./data/cringe.txt", "r") as f:
                    lines = f.readlines()
                with open("./data/cringe.txt", "w") as f:
                    for line in lines:
                        if line.strip("\n") != url:
                            f.write(line)
                await channel_embed(ctx, 'Removed', 'I guess that wasn\'nt cringe enough')
                logging.info(f'{ctx.author.id} removed a cringe')
            else:
                await error_embed(ctx, 'That url does not exist in the cringe db')

    @cringe.command()
    @commands.check(helper_group)
    async def add(self, ctx, url=None):
        if len(ctx.message.attachments) == 0 and url is None:
            await error_embed(ctx, 'You need to give a url or attachment to add cringe')
        else:
            if ctx.message.attachments[0].url.lower().endswith(('.png', '.jpeg', '.jpg', '.gif')) or (url.startswith('https://') and url.endswith(('.png', '.jpeg', '.jpg', '.gif'))):
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
            else:
                await error_embed(ctx, 'Invalid attachment, must be `.png`, `.gif`, `.jpeg`, or `.jpg` or an image url')


def setup(bot):
    bot.add_cog(Cringe(bot))
