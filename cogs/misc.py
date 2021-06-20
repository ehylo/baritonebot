import discord
import main
from time import time
from random import SystemRandom
from discord.ext import commands
from cogs.help import Help


rock_img = 'https://cdn.discordapp.com/attachments/819449117561585704/833146899216334850/rock.png'
paper_img = 'https://cdn.discordapp.com/attachments/819449117561585704/833146893822590997/paper.png'
scissors_img = 'https://cdn.discordapp.com/attachments/819449117561585704/833146896662921236/scissors.png'
tie = 'does nothing to'
rock_scissors = 'Rock crushes Scissors'
paper_rock = 'Paper covers Rock'
scissors_paper = 'Scissors cuts Paper'


async def computer_rps(ctx, choice_num, choice, image):
    comp_choice = [SystemRandom().randrange(3)][0]+1
    if comp_choice == 1:
        str_compchoice = 'Rock'
    elif comp_choice == 2:
        str_compchoice = 'Paper'
    else:
        str_compchoice = 'Scissors'
    if choice_num == comp_choice:
        title = 'We Tied :|'
        main.stat_update(r'UPDATE stats SET tied = tied + 1 WHERE user_id = %s', ctx.author.id)
        action = f'{choice} {tie} {str_compchoice}'
    elif choice_num+1 < comp_choice or choice_num-1 == comp_choice:
        title = 'You Won! :)'
        main.stat_update(r'UPDATE stats SET won = won + 1 WHERE user_id = %s', ctx.author.id)
        if choice_num == 1:
            action = rock_scissors
        elif choice_num == 2:
            action = paper_rock
        else:
            action = scissors_paper
    else:
        if comp_choice == 1:
            action = rock_scissors
        elif comp_choice == 2:
            action = paper_rock
        else:
            action = scissors_paper
        title = 'You lost :('
        main.stat_update(r'UPDATE stats SET lost = lost + 1 WHERE user_id = %s', ctx.author.id)
    await main.channel_embed(ctx, title, action, image)


async def top_formatter(self, topp):
    desc, x = '', 0
    for i in topp[:10]:
        x += 1
        u_id, txp = int(str(i).split(' ')[1][:-1]), int(str(i).split(' ')[0][1:-1])
        try:
            user = (await self.bot.get_guild(main.ids(1)).fetch_member(u_id)).name
        except discord.NotFound:
            try:
                user = (await self.bot.fetch_user(u_id)).name
            except discord.NotFound:
                user = u_id
        desc += f'**{x}.** {user} - `{txp}`\n'
    return desc


class Misc(commands.Cog):
    def __init__(self, bot):
        """Returns if the user won or other emebeds for the commands."""
        self.bot = bot

    @commands.group(invoke_without_command=True, case_insensitive=True, aliases=['t'])
    async def top(self, ctx):
        main.cur.execute('SELECT exp, user_id FROM stats ORDER BY exp DESC')
        await main.channel_embed(ctx, 'Top XP leaderboard', await top_formatter(self, main.cur.fetchall()))

    @top.command()
    async def messages(self, ctx):
        em_v = discord.Embed(color=int(main.values(1), 16), title='Top Messages/Edits/Deletes/Responses leaderboard')
        main.cur.execute('SELECT messages, user_id FROM stats ORDER BY messages DESC')
        em_v.add_field(name='Messages:', value=await top_formatter(self, main.cur.fetchall()))
        board = await ctx.send(embed=em_v)
        main.cur.execute('SELECT edited, user_id FROM stats ORDER BY edited DESC')
        em_v.add_field(name='Edits:', value=await top_formatter(self, main.cur.fetchall()))
        await board.edit(embed=em_v)
        main.cur.execute('SELECT deleted, user_id FROM stats ORDER BY deleted DESC')
        em_v.add_field(name='Deletes:', value=await top_formatter(self, main.cur.fetchall()))
        await board.edit(embed=em_v)
        main.cur.execute('SELECT triggered_responses, user_id FROM stats ORDER BY triggered_responses DESC')
        em_v.add_field(name='Respones:', value=await top_formatter(self, main.cur.fetchall()))
        await board.edit(embed=em_v)

    @top.command(aliases=['flip'])
    async def coin(self, ctx):
        em_v = discord.Embed(color=int(main.values(1), 16), title='Top Heads/Tails leaderboard')
        main.cur.execute('SELECT heads, user_id FROM stats ORDER BY heads DESC')
        em_v.add_field(name='Heads:', value=await top_formatter(self, main.cur.fetchall()))
        board = await ctx.send(embed=em_v)
        main.cur.execute('SELECT tails, user_id FROM stats ORDER BY tails DESC')
        em_v.add_field(name='Tails:', value=await top_formatter(self, main.cur.fetchall()))
        await board.edit(embed=em_v)

    @top.command(aliases=['rps'])
    async def spr(self, ctx):
        em_v = discord.Embed(color=int(main.values(1), 16), title='Top Rock/Paper/Scissors/Won/Lost/Tied leaderboard')
        main.cur.execute('SELECT rock, user_id FROM stats ORDER BY rock DESC')
        em_v.add_field(name='Rock:', value=await top_formatter(self, main.cur.fetchall()))
        board = await ctx.send(embed=em_v)
        main.cur.execute('SELECT paper, user_id FROM stats ORDER BY paper DESC')
        em_v.add_field(name='Paper:', value=await top_formatter(self, main.cur.fetchall()))
        await board.edit(embed=em_v)
        main.cur.execute('SELECT scissors, user_id FROM stats ORDER BY scissors DESC')
        em_v.add_field(name='Scissors:', value=await top_formatter(self, main.cur.fetchall()))
        await board.edit(embed=em_v)
        main.cur.execute('SELECT won, user_id FROM stats ORDER BY won DESC')
        em_v.add_field(name='Won:', value=await top_formatter(self, main.cur.fetchall()))
        await board.edit(embed=em_v)
        main.cur.execute('SELECT lost, user_id FROM stats ORDER BY lost DESC')
        em_v.add_field(name='Lost:', value=await top_formatter(self, main.cur.fetchall()))
        await board.edit(embed=em_v)
        main.cur.execute('SELECT tied, user_id FROM stats ORDER BY tied DESC')
        em_v.add_field(name='Tied:', value=await top_formatter(self, main.cur.fetchall()))
        await board.edit(embed=em_v)

    @commands.command()
    async def flip(self, ctx):
        c = [SystemRandom().randrange(2)][0]+1
        if c == 1:
            main.stat_update(r'UPDATE stats SET heads = heads + 1 WHERE user_id = %s', ctx.author.id)
            await main.channel_embed(ctx, '🗣 Heads! 🗣')
        else:
            main.stat_update(r'UPDATE stats SET tails = tails + 1 WHERE user_id = %s', ctx.author.id)
            await main.channel_embed(ctx, '🦅 Tails! 🦅')

    @commands.group(invoke_without_command=True, case_insensitive=True)
    async def rps(self, ctx):
        return await Help.rps(self, ctx)

    @rps.command(aliases=['r'])
    async def rock(self, ctx):
        main.stat_update(r'UPDATE stats SET rock = rock + 1 WHERE user_id = %s', ctx.author.id)
        await computer_rps(ctx, 1, 'Rock', rock_img)

    @rps.command(aliases=['p'])
    async def paper(self, ctx):
        main.stat_update(r'UPDATE stats SET paper = paper + 1 WHERE user_id = %s', ctx.author.id)
        await computer_rps(ctx, 2, 'Paper', paper_img)

    @rps.command(aliases=['s'])
    async def scissors(self, ctx):
        main.stat_update(r'UPDATE stats SET scissors = scissors + 1 WHERE user_id = %s', ctx.author.id)
        await computer_rps(ctx, 3, 'Scissors', scissors_img)

    @commands.command()
    async def daily(self, ctx):
        main.cur.execute('SELECT daily FROM stats WHERE user_id = %s', (ctx.author.id,))
        daily_check = str(main.cur.fetchone())
        utc = (int(time() % 86400) - 3600)
        if utc <= 0:
            utc += 86400
        next_time = main.time_convert(86400 - utc)
        if daily_check != '(True,)':
            main.stat_update(r'UPDATE stats SET daily = true WHERE user_id = %s', ctx.author.id)
            main.stat_update(r'UPDATE stats SET exp = exp + 100 WHERE user_id = %s', ctx.author.id)
            print(f'{ctx.author.id} claimed their dailies')
            await main.channel_embed(ctx, 'Claimed!', f'You have claimed your daily today and gained 100 exp!\nYou can claim your next daily in {next_time}')
        else:
            await main.channel_embed(ctx, 'Oh no!', f'Unfortunately you have already claimed your dailies today\nCome back in {next_time} to claim your next daily!')

    @rps.command()
    async def ls(self, ctx, choice=None):
        lizard_img = 'https://cdn.discordapp.com/attachments/819449117561585704/833170722050408499/lizard.png'
        spock_img = 'https://cdn.discordapp.com/attachments/819449117561585704/833170723908354058/spock.png'
        rock_lizard = 'Rock crushes Lizard'
        paper_spock = 'Paper disproves Spock'
        scissors_lizard = 'Scissors decapitates Lizard'
        lizard_paper = 'Lizard eats Paper'
        lizard_spock = 'Lizard poisons Spock'
        spock_rock = 'Spock vaporizes Rock'
        spock_scissors = 'Spock smashes Scissors'
        if (choice is None) or (choice.lower() not in ['rock', 'paper', 'scissors', 'lizard', 'spock']):
            return await Help.rpsls(self, ctx)
        if choice.lower() == 'rock':
            main.stat_update(r'UPDATE stats SET rock = rock + 1 WHERE user_id = %s', ctx.author.id)
            user_choice = 1
            image = rock_img
        elif choice.lower() == 'paper':
            main.stat_update(r'UPDATE stats SET paper = paper + 1 WHERE user_id = %s', ctx.author.id)
            user_choice = 2
            image = paper_img
        elif choice.lower() == 'scissors':
            main.stat_update(r'UPDATE stats SET scissors = scissors + 1 WHERE user_id = %s', ctx.author.id)
            user_choice = 3
            image = scissors_img
        elif choice.lower() == 'lizard':
            main.stat_update(r'UPDATE stats SET lizard = lizard + 1 WHERE user_id = %s', ctx.author.id)
            user_choice = 4
            image = lizard_img
        else:
            main.stat_update(r'UPDATE stats SET spock = spock + 1 WHERE user_id = %s', ctx.author.id)
            user_choice = 5
            image = spock_img
        comp_choice = [SystemRandom().randrange(5)][0]+1
        if user_choice == 1 and comp_choice == 2:
            title = 'You lost :('
            action = paper_rock
        elif user_choice == 1 and comp_choice == 5:
            title = 'You lost :('
            action = spock_rock
        elif user_choice == 1 and comp_choice == 3:
            title = 'You Won! :)'
            action = rock_scissors
        elif user_choice == 1 and comp_choice == 4:
            title = 'You Won! :)'
            action = rock_lizard
        elif user_choice == 2 and comp_choice == 3:
            title = 'You lost :('
            action = scissors_paper
        elif user_choice == 2 and comp_choice == 4:
            title = 'You lost :('
            action = lizard_paper
        elif user_choice == 2 and comp_choice == 1:
            title = 'You Won! :)'
            action = paper_rock
        elif user_choice == 2 and comp_choice == 5:
            title = 'You Won! :)'
            action = paper_spock
        elif user_choice == 3 and comp_choice == 1:
            title = 'You lost :('
            action = rock_scissors
        elif user_choice == 3 and comp_choice == 5:
            title = 'You lost :('
            action = spock_scissors
        elif user_choice == 3 and comp_choice == 2:
            title = 'You Won! :)'
            action = scissors_paper
        elif user_choice == 3 and comp_choice == 4:
            title = 'You Won! :)'
            action = scissors_lizard
        elif user_choice == 4 and comp_choice == 1:
            title = 'You lost :('
            action = rock_lizard
        elif user_choice == 4 and comp_choice == 3:
            title = 'You lost :('
            action = scissors_lizard
        elif user_choice == 4 and comp_choice == 2:
            title = 'You Won! :)'
            action = lizard_paper
        elif user_choice == 4 and comp_choice == 5:
            title = 'You Won! :)'
            action = lizard_spock
        elif user_choice == 5 and comp_choice == 2:
            title = 'You lost :('
            action = paper_spock
        elif user_choice == 5 and comp_choice == 4:
            title = 'You lost :('
            action = lizard_spock
        elif user_choice == 5 and comp_choice == 1:
            title = 'You Won! :)'
            action = spock_rock
        elif user_choice == 5 and comp_choice == 3:
            title = 'You Won! :)'
            action = spock_scissors
        else:
            action = f'{choice} {tie} {choice}'
            title = 'We Tied :|'
            main.stat_update(r'UPDATE stats SET tied = tied + 1 WHERE user_id = %s', ctx.author.id)
        if title == 'You Won! :)':
            main.stat_update(r'UPDATE stats SET won = won + 1 WHERE user_id = %s', ctx.author.id)
        elif title == 'You lost :(':
            main.stat_update(r'UPDATE stats SET lost = lost + 1 WHERE user_id = %s', ctx.author.id)
        await main.channel_embed(ctx, title,  action, image)


def setup(bot):
    bot.add_cog(Misc(bot))
