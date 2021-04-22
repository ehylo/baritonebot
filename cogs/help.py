from discord.ext import commands
from const import channel_embed, help_embed


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True, case_insensitive=True, aliases=['h'])
    async def help(self, ctx):
        desc = '\
            \u2022 `help admin` - Admin commands \
            \n\u2022 `help mod` - Moderator commands \
            \n\u2022 `help helper` - Helper commands \
            \n\u2022 `help everyone` - Commands available to everyone'
        await channel_embed(ctx, 'List of help categories:', desc)
        
    @help.command(aliases=['a'])
    async def admin(self, ctx):
        field_value = '\
            \u2022 `extension(ext) <reload(r)|unload(u)|load(ld)|list(l)> <[extension]|all>` \
            \n\u2022 `unban(ub) <[user]>` \
            \n\u2022 `embedcolor(ec) <default(d)|[hex color]>` \
            \n\u2022 `prefix(pf) <default(d)|[prefix]>` \
            \n\u2022 `<un>exempt(ex) <help|list(l)>` \
            \n\u2022 `rule(r) <add(a)|remove(r)> <[number]> <[title]> <[description]>` \
            \n*+ all lower commands*'
        await help_embed(ctx, 'Admin', '`help <command>` to get command info or give no arguments if it does not have `<help>`', field_value, 'Commands:')

    @help.command(aliases=['m'])
    async def mod(self, ctx):
        field_value = '\
            \u2022 `ban(b|rm) <[user]> <[reason]>` \
            \n\u2022 `response(rp) <add(a)|remove(r)> <[regex]|[number]> <[title]> <[description]>` \
            \n\u2022 `blacklist(bl) <add(a)|remove(r)> <word]>` \
            \n\u2022 `cringe(c) <remove(r)>` \
            \n\u2022 `kick(k) <[user]> <[reason]>` \
            \n\u2022 `clear(cl|pg|purge) <[number]|[user]> <[number]>` \
            \n\u2022 `unmute(um) <[user]>` \
            \n\u2022 `nick(n) <default(d)|remove(r)|[name]>` \
            \n\u2022 `status(s) <default(d)|[presence]>` \
            \n\u2022 `emote(em) <[name]> <[image attachment]|[image url]>` \
            \n\u2022 `embed(eb) <[channel]|here(h)> <[title]> <[description]>` \
            \n*+ all lower commands*'
        await help_embed(ctx, 'Moderator', '`help <command>` to get command info or give no arguments', field_value, 'Commands:')

    @help.command(aliases=['h'])
    async def helper(self, ctx):
        field_value = '\
            \u2022 `mute(m) <[user]> <[time(d=days, h=hours, m=minutes)]|[reason]> <[reason]>` \
            \n\u2022 `response(rp) <details(d)|list(l)> <[number]>` \
            \n\u2022 `blacklist(bl) <list(l)>` \
            \n\u2022 `cringe(c) <add(a)> <[image url]|[image attachment]>` \
            \n*+ all lower commands*'
        await help_embed(ctx, 'Helper', '`help <command>` to get command info or give no arguments if it does not have `<help>`', field_value, 'Commands:')

    @help.command(aliases=['e'])
    async def everyone(self, ctx):
        field_value = '\
            \u2022 `rule(r)<s> <[number]>` \
            \n\u2022 `ping(p) <help>` \
            \n\u2022 `rps <rock(r)|paper(p)|scissors(s)>` \
            \n\u2022 `flip <help>` \
            \n\u2022 `cringe(c) <help>` \
            \n\u2022 `serverinfo(si) <help>` \
            \n\u2022 `userinfo(ui) <me|[user]>` \
            \n\u2022 `<un>releases <help>` \
            \n\u2022 `<un>ignore <help>` \
            \n\u2022 `optout <I am sure>` \
            \n\u2022 `help(h) <admin(a)|mod(m)|helper(h)|everyone(e)>`'
        await help_embed(ctx, 'Available to everyone:', '`help <command>` to get command info or give no arguments if it does not have `<help>`', field_value, 'Commands:')

    @help.command()
    async def unban(self, ctx):
        await help_embed(ctx, 'Unban', 'Unbans the specified user ID', '`unban(ub) <[user]>`')

    @help.command()
    async def unmute(self, ctx):
        await help_embed(ctx, 'Unmute', 'Unmutes the specified member', '`unmute(um) <[user]>`')

    @help.command()
    async def ban(self, ctx):
        await help_embed(ctx, 'Ban', 'Bans the specified member', '`ban(b|rm) <[user]> <[reason]>`')

    @help.command()
    async def mute(self, ctx):
        await help_embed(ctx, 'Mute', 'Mutes the specified member indefinitely or for the specified amount of time', '`mute(m) <[user]> <[time(d=days, h=hours, m=minutes)]|[reason]> <[reason]>`')

    @help.command()
    async def kick(self, ctx):
        await help_embed(ctx, 'Kick', 'Kicks the specified member', '`kick(k) <[user]> <[reason]>`')

    @help.command()
    async def blacklist(self, ctx):
        await help_embed(ctx, 'Blacklist', 'Command to add/remove a word on the blacklist or show a list of all of the blacklisted words', '`blacklist(bl) <add(a)|remove(r)|list(l)> <[word]>`')

    @help.command()
    async def embed(self, ctx):
        await help_embed(ctx, 'Embed', 'Sends an embed to the specified channel with the specified title/description', '`embed(eb) <[channel]|here(h)> <[title]> <[description]>`')

    @help.command()
    async def emote(self, ctx):
        await help_embed(ctx, 'Emote', 'Creates an emote with the specified name and provided image', '`emote(em) <[name]> <[image attachment]|[image url]>` - you can attach an image instead of having a url')

    @help.command()
    async def clear(self, ctx):
        await help_embed(ctx, 'Clear', 'Clears the specified amount of messages in that channel or give a user to clear a specific amount of their messages', '`clear(cl|pg|purge) <[number]|[user]> <[number]>`')

    @help.command()
    async def optout(self, ctx):
        await help_embed(ctx, 'Opt-Out', 'You will be banned from the server', '`optout <I am sure>`')

    @help.command()
    async def response(self, ctx):
        await help_embed(ctx, 'Response', 'Command to control responses, can add/remove them or list/get details of them \n*use [this](https://regexr.com/) website to make the regex*', '`response(rp) <add(a)|remove(r)|details(d)|list(l)> <[regex]|[number]> <[title]> <[description]>`')

    @help.command()
    async def rule(self, ctx):
        await help_embed(ctx, 'Rules', 'Sends the specified rule, or all of them, or add/remove a rule', '`rule(r)<s> <add(a)|remove(r)|[number]> <[number]> <[title]> <[description]>`')

    @help.command()
    async def prefix(self, ctx):
        await help_embed(ctx, 'Prefix', 'Allows you to set the command prefix for the bot', '`prefix(pf) <default(d)|[prefix]>`')

    @help.command()
    async def embedcolor(self, ctx):
        await help_embed(ctx, 'Embedcolor', 'Allows you to set the embedcolor for all the embeds the bot sends', '`embedcolor(ec) <default(d)|[hex color]>`')

    @help.command()
    async def nick(self, ctx):
        await help_embed(ctx, 'Nick', 'Allows you to set the bot\'s nick in this server', '`nick(n) <default(d)|remove(r)|[name]>`')

    @help.command()
    async def status(self, ctx):
        await help_embed(ctx, 'Status', 'Allows you to set the bot\'s status', '`status(s) <default(d)|[presence]>`')

    @help.command()
    async def cringe(self, ctx):
        await help_embed(ctx, 'Cringe', 'Either recieve a random cringe or add/remove a cringe', '`cringe(c) <add(a)|remove(r)|help> <[image url]|[image attachment]>` - you can attach an image instead of having a url')

    @help.command()
    async def ignore(self, ctx):
        await help_embed(ctx, 'Ignored', 'Add/remove the ignored role, if you have this role your messages will not trigger most of the regex responses', '`<un>ignore <help>`')

    @help.command()
    async def releases(self, ctx):
        await help_embed(ctx, 'Releases', 'Add/remove the releases role, if you have this role you will be pinged when a new release comes out', '`<un>releases <help>`')

    @help.command()
    async def ping(self, ctx):
        await help_embed(ctx, 'huh', 'why would you need help for ping? did you think it pings someone specific? xD', '`ping(p) <help>`')

    @help.command()
    async def rps(self, ctx):
        await help_embed(ctx, 'Rock, Paper, Scissors', 'Play a game of rock, paper, scissors against a bot', '`rps <rock(r)|paper(p)|scissors(s)>`')

    @help.command()
    async def rpsls(self, ctx):
        await help_embed(ctx, 'Rock, Paper, Scissors, Lizard, Spock', 'Play a game of rock, paper, scissors, lizard, spock against a bot', '`rps ls <rock|paper|scissors|lizard|spock>`', None, 'https://cdn.discordapp.com/attachments/819449117561585704/833201595189035008/Rock_paper_scissors_lizard_spock.png')

    @help.command()
    async def flip(self, ctx):
        await help_embed(ctx, 'Coin Flip', 'Randomly flips a coin for you, for when you need someone else to decide something for you', '`flip <help>`')

    @help.command()
    async def serverinfo(self, ctx):
        await help_embed(ctx, 'Server Information', 'Shows information about the server', '`serverinfo(si) <help>`')

    @help.command()
    async def userinfo(self, ctx):
        await help_embed(ctx, 'User Information', 'Shows information about the given member/user', '`userinfo(ui) <me|[user]>`')

    @help.command()
    async def extension(self, ctx):
        await help_embed(ctx, 'Extension', 'Loads, unloads, or reloads the specified extension or lists all of the extensions', '`extension(ext) <reload(r)|unload(u)|load(ld)|list(l)> <[extension]|all>`')

    @help.command()
    async def exempt(self, ctx):
        await help_embed(ctx, 'Exempt', 'Allows you to make the current channel exempted from the blacklist and regex responses, or list the current channels exempted', '`<un>exempt(ex) <help|list(l)>`')


def setup(bot):
    bot.add_cog(Help(bot))
