import logging
from cogs.help import Help
from discord.ext import commands
from const import error_embed, admin_group, channel_embed, baritoneDiscord


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
            num_lines = sum(1 for _ in open("./data/exemptchannels.txt"))
            word = str(ctx.channel.id)
            f = open("./data/exemptchannels.txt", "r")
            lines = f.readlines()
            f.close()
            if num_lines == 0:
                f = open("./data/exemptchannels.txt", "a")
                f.write(f'{word}')
                f.close()
                await channel_embed(ctx, 'Exempted', f'The channel {ctx.channel.mention} is now exempted from the blacklist, regex responses, and message logging')
                logging.info(f'{ctx.author.id} added a channel ({word}) to the exemptchannels')
            else:
                if word not in [sub.replace('\n', '') for sub in lines]:
                    f = open("./data/exemptchannels.txt", "a")
                    f.write(f'\n{word}')
                    f.close()
                    await channel_embed(ctx, 'Exempted', f'The channel {ctx.channel.mention} is now exempted from the blacklist, regex responses, and message logging')
                    logging.info(f'{ctx.author.id} added a channel ({word}) to the exemptchannels')
                else:
                    await error_embed(ctx, 'This channel is already on the exempt list')

    @exempt.command(aliases=['list', 'l'])
    @commands.check(admin_group)
    async def show(self, ctx):  # totally didn't make this 'show' so I didn't have to make a new class :whistle:
        slist = open("./data/exemptchannels.txt", "r")
        mlist = []
        for line in slist:
            exm_chl = self.bot.get_channel(int(line))
            mlist.append(str(exm_chl.id))
        slist.close()
        await channel_embed(ctx, f'Exempted Channels ({len(mlist)})', f'<#{(">, <#".join(mlist))}>')

    @commands.group(invoke_without_command=True, case_insensitive=True, aliases=['unex'])
    @commands.check(admin_group)
    async def unexempt(self, ctx, arg=None):
        if (arg is not None) and (arg.lower() == 'help'):
            await Help.exempt(self, ctx)
        elif ctx.guild is None:
            await error_embed(ctx, 'You cannot use this command in DMs')
        else:
            num_lines = sum(1 for _ in open("./data/exemptchannels.txt"))
            tlines = 1
            f = open("./data/exemptchannels.txt", "r")
            lines = f.readlines()
            res = [sub.replace('\n', '') for sub in lines]
            word = str(ctx.channel.id)
            if word in res:
                with open("./data/exemptchannels.txt", "r") as f:
                    lines = f.readlines()
                with open("./data/exemptchannels.txt", "w") as f:
                    for line in lines:
                        tlines += 1
                        if tlines == num_lines and (line.strip("\n") == word):
                            with open("./data/exemptchannels.txt", "r") as d:
                                llines = d.readlines()
                            with open("./data/exemptchannels.txt", "w") as d:
                                for lline in llines:
                                    if tlines != num_lines and lline.strip("\n") != word:
                                        f.write(lline)
                                    elif tlines == num_lines:
                                        sline = lline.strip('\n')
                                        f.write(sline)
                            d.close()
                        elif tlines != num_lines and line.strip("\n") != word:
                            f.write(line)
                        elif tlines == num_lines:
                            sline = line.strip('\n')
                            f.write(sline)
                await channel_embed(ctx, 'Un-exempted', f'The channel {ctx.channel.mention} is no longer exempted from the blacklist and regex responses')
                logging.info(f'{ctx.author.id} removed a channel ({word}) from the exemptchannels')
                f.close()
            else:
                await error_embed(ctx, 'This channel is not exempted')

    @unexempt.command(aliases=['l'])
    @commands.check(admin_group)
    async def list(self, ctx):
        slist = open("./data/exemptchannels.txt", "r")
        channels = self.bot.get_guild(baritoneDiscord).text_channels
        clist = []
        klist = []
        for line in slist:
            exm_chl = self.bot.get_channel(int(line))
            clist.append(exm_chl)
        flist = [x for x in channels if x not in clist]
        for channel in flist:
            klist.append(str(channel.id))
        slist.close()
        await channel_embed(ctx, f'Unexempted Channels ({len(flist)})', f'<#{(">, <#".join(klist))}>')


def setup(bot):
    bot.add_cog(Exempt(bot))
