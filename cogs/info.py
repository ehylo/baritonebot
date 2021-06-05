import discord
import main
import requests
import re
from time import time
from discord.ext import commands
from cogs.help import Help


async def info_embed(ctx, member, title, field1, field2, field3, value):
    em_v = discord.Embed(color=int(main.values(1), 16),  title=title)
    em_v.add_field(name='Mention:', value=member.mention, inline=True)
    em_v.add_field(name='Status:', value=field1, inline=True)
    em_v.add_field(name='Created:', value=member.created_at.strftime('%B %d, %Y at %I:%M:%S %p').lstrip('0').replace(' 0', ' '), inline=False)
    em_v.add_field(name='Joined:', value=field2, inline=False)
    em_v.add_field(name=field3, value=value, inline=False)
    em_v.set_author(name=f'{member.name}#{member.discriminator}', icon_url=member.avatar_url)
    em_v.set_footer(text=f'ID: {member.id}')
    em_v.set_thumbnail(url=member.avatar_url)
    await ctx.send(embed=em_v)


async def varistuff(ctx, member, ismember):
    if ismember is True:
        await info_embed(ctx, member, 'Member Information:', member.status, member.joined_at.strftime('%B %d, %Y at %I:%M:%S %p').lstrip('0').replace(' 0', ' '), f'Roles ({len(member.roles)-1}):', (' '.join([str(r.mention) for r in member.roles][1:])+'\u200b'))
    elif ismember is False:
        await info_embed(ctx, member, 'User Information:', 'API doesn\'t support this yet', 'User has not joined the baritone server yet', 'Default avatar color:', member.default_avatar)


async def setting_searcher(ctx, setting, link):
    settings = []
    description = ''
    for x in requests.get(link).content.decode('utf-8').split('/**')[2:-4]:
        clean = ' '.join(x.split())
        default_setting = clean.split('*/', 1)[1][:-2].split(' = new Setting<>(', 1)[1]
        # Edge cases below yay \o/
        if default_setting.startswith('new ArrayList<>'):
            if '( )' in default_setting:
                default = '()'
            elif 'Item.getItem' in default_setting:
                default = '(dirt, cobblestone, netherrack, stone)'
            else:
                default = '(' + ''.join(default_setting.split('Blocks.')[1:])[:-3].lower() + ')'
        elif default_setting.startswith('new Vec'):
            default = default_setting.split('3i')[1]
        else:
            default = default_setting

        set_dict = {
            'description': clean.split('*/')[0][2:-1].replace(' * <p> * ', '\n').replace(' * ', ' '),
            'title': clean.split('*/')[1][21:-2].split(' = new', 1)[0].split('> ')[1],
            'type': clean.split('*/')[1].split('> ', 1)[0].split('Setting<')[1],
            'default': default
        }
        settings.append(set_dict.copy())
    for x in settings:
        if re.search(setting.lower(), x['title'].lower()) is not None:
            description += f"**[{x['title']}](https://baritone.leijurv.com/baritone/api/Settings.html#{x['title']})** | __{x['type']}__ | *Default:* `{x['default']}`\n{x['description']}\n\n"
    if description == '':
        description = 'There was no settings found for that search :('
    em_v = discord.Embed(color=int(main.values(1), 16), description=description)
    em_v.set_footer(text=f'{ctx.author.name} | ID: {ctx.author.id}', icon_url=ctx.author.avatar_url)
    await ctx.send(embed=em_v)


class Info(commands.Cog):
    def __init__(self, bot):
        """Returns embeds for all the info commands."""
        self.bot = bot

    @commands.command(aliases=['p'])
    async def ping(self, ctx):
        await main.channel_embed(ctx, f'Pong! 🏓 ({round(self.bot.latency * 1000)}ms)', None)

    @commands.group(invoke_without_command=True, case_insensitive=True, aliases=['ui'])
    async def userinfo(self, ctx, user_id=None):
        b_guild = self.bot.get_guild(main.ids(1))
        try:
            user_men = str(ctx.message.raw_mentions[0])
        except IndexError:
            user_men = ''
        if user_id is None:
            await Help.userinfo(self, ctx)
        else:
            if user_men != '':
                clear_member = await self.bot.fetch_user(int(user_men))  # get the user if they mentioned
            elif (user_id.isdigit()) and (len(user_id) == 18):
                clear_member = await self.bot.fetch_user(int(user_id))  # get the user if they gave an ID
            else:
                clear_member = b_guild.get_member_named(user_id)  # get the member if they gave a name with/without discrimitor
            if clear_member is None:
                await main.error_embed(ctx, 'The user you gave is invalid')
            else:
                if b_guild.get_member(clear_member.id) is not None:
                    member = b_guild.get_member(clear_member.id)
                    await varistuff(ctx, member, ismember=True)
                else:
                    member = await self.bot.fetch_user(clear_member.id)
                    await varistuff(ctx, member, ismember=False)

    @userinfo.command()
    async def me(self, ctx):
        b_guild = self.bot.get_guild(main.ids(1))
        member_check = b_guild.get_member(ctx.author.id)
        if member_check is not None:
            await varistuff(ctx, member_check, ismember=True)
        else:
            await varistuff(ctx, ctx.author, ismember=False)

    @commands.command(aliases=['si'])
    async def serverinfo(self, ctx):
        b_guild = self.bot.get_guild(main.ids(1))
        em_v = discord.Embed(color=int(main.values(1), 16),  title=f'Server Information: {b_guild.name}')
        em_v.add_field(name='Owner:', value=f'{b_guild.owner} (ID: {b_guild.owner_id})', inline=False)
        em_v.add_field(name='Description:', value=b_guild.description, inline=False)
        em_v.add_field(name='Created:', value=b_guild.created_at.strftime('%B %d, %Y at %I:%M:%S %p').lstrip('0').replace(' 0', ' '), inline=False)
        em_v.add_field(name='Region:', value=b_guild.region, inline=False)
        em_v.add_field(name=f'Roles ({len(b_guild.roles)-1}):', value=(' '.join([str(r.mention) for r in b_guild.roles][1:])+'\u200b'), inline=False)
        em_v.add_field(name='Text Channels:', value=str(len(b_guild.text_channels)), inline=True)
        em_v.add_field(name='Voice Channels:', value=str(len(b_guild.voice_channels)), inline=True)
        em_v.add_field(name='Members:', value=b_guild.member_count, inline=True)
        em_v.set_footer(text=f'ID: {b_guild.id}')
        em_v.set_thumbnail(url=b_guild.icon_url)
        await ctx.send(embed=em_v)

    @commands.command(aliases=['about'])
    async def info(self, ctx):
        em_v = discord.Embed(
            color=int(main.values(1), 16),
            description=f'Current prefix: `{main.values(0)}`'
                        f'\n\n__**Info:**__'
                        f'\n\u2022 Made by Flurr#0001'
                        f'\n\u2022 Written in [python](https://www.python.org/) using the [discord.py](https://github.com/Rapptz/discord.py) library'
                        f'\n\u2022 Uses a [PostgreSQL](https://www.postgresql.org/) database'
                        f'\n\n__**Links:**__'
                        f'\n\u2022 [Bot source code on GitHub](https://github.com/Flurrrr/baritonebot)'
                        f'\n\u2022 [Main Baritone GitHub repo](https://github.com/cabaletta/baritone)'
                        f'\n\u2022 [Invite to Baritone discord server](https://discord.gg/s6fRBAUpmr)'
        )
        em_v.set_author(name='Baritone Bot', url='https://github.com/Flurrrr/baritonebot', icon_url=self.bot.user.avatar_url)
        em_v.set_footer(text=f'{ctx.author.name} | ID: {ctx.author.id}', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=em_v)

    @commands.command(aliases=['ut'])
    async def uptime(self, ctx):
        await main.channel_embed(ctx, 'Uptime', main.time_convert(int(time()) - main.start_time))

    @commands.command()
    async def opspt(self, ctx, setting=None):
        if setting is None:
            await Help.opspt(self, ctx)
        else:
            await setting_searcher(ctx, setting, 'https://raw.githubusercontent.com/cabaletta/baritone/v1.6.3/src/api/java/baritone/api/Settings.java')

    @commands.command()
    async def optpf(self, ctx, setting=None):
        if setting is None:
            await Help.optpf(self, ctx)
        else:
            await setting_searcher(ctx, setting, 'https://raw.githubusercontent.com/cabaletta/baritone/v1.2.15/src/api/java/baritone/api/Settings.java')


def setup(bot):
    bot.add_cog(Info(bot))
