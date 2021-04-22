import random
from discord.ext import commands
from cogs.help import Help
from const import channel_embed


rock_img = 'https://cdn.discordapp.com/attachments/819449117561585704/833146899216334850/rock.png'
paper_img = 'https://cdn.discordapp.com/attachments/819449117561585704/833146893822590997/paper.png'
scissors_img = 'https://cdn.discordapp.com/attachments/819449117561585704/833146896662921236/scissors.png'
tie = 'does nothing to'
rock_scissors = 'Rock crushes Scissors'
paper_rock = 'Paper covers Rock'
scissors_paper = 'Scissors cuts Paper'


async def computer_rps(ctx, choice_num, choice, image):
    comp_choice = random.randint(1, 3)
    if comp_choice == 1:
        str_compchoice = 'Rock'
    elif comp_choice == 2:
        str_compchoice = 'Paper'
    else:
        str_compchoice = 'Scissors'
    if choice_num == comp_choice:
        title = 'We Tied :|'
        action = f'{choice} {tie} {str_compchoice}'
    elif choice_num+1 < comp_choice or choice_num-1 == comp_choice:
        title = 'You Won! :)'
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
    await channel_embed(ctx, title, action, image)


class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['p'])
    async def ping(self, ctx, arg=None):
        if (arg is not None) and (arg.lower() == 'help'):
            await Help.ping(self, ctx)
        else:
            await channel_embed(ctx, f'Pong! 🏓 ({round(self.bot.latency * 1000)}ms)', None)

    @commands.command()
    async def flip(self, ctx, arg=None):
        if (arg is not None) and (arg.lower() == 'help'):
            await Help.flip(self, ctx)
        else:
            c = random.randint(1, 2)
            if c == 1:
                await channel_embed(ctx, '🗣 Heads! 🗣')
            else:
                await channel_embed(ctx, '🦅 Tails! 🦅')

    @commands.group(invoke_without_command=True, case_insensitive=True)
    async def rps(self, ctx):
        await Help.rps(self, ctx)

    @rps.command(aliases=['r'])
    async def rock(self, ctx):
        await computer_rps(ctx, 1, 'Rock', rock_img)

    @rps.command(aliases=['p'])
    async def paper(self, ctx):
        await computer_rps(ctx, 2, 'Paper', paper_img)

    @rps.command(aliases=['s'])
    async def scissors(self, ctx):
        await computer_rps(ctx, 3, 'Scissors', scissors_img)

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
            await Help.rpsls(self, ctx)
        else:
            if choice.lower() == 'rock':
                user_choice = 1
                image = rock_img
            elif choice.lower() == 'paper':
                user_choice = 2
                image = paper_img
            elif choice.lower() == 'scissors':
                user_choice = 3
                image = scissors_img
            elif choice.lower() == 'lizard':
                user_choice = 4
                image = lizard_img
            else:
                user_choice = 5
                image = spock_img
            comp_choice = random.randint(1, 5)
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
            await channel_embed(ctx, title,  action, image)


def setup(bot):
    bot.add_cog(Misc(bot))
