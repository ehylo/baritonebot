import discord
import cogs
import logging
from discord.ext import commands
from cogs.const import channel_embed, help_embed, error_embed

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def help(self, ctx):
        title = 'List of help categories:'
        desc = '\
            \u2022 `help admin` - Admin commands \
            \n\u2022 `help mod` - Moderator commands \
            \n\u2022 `help helper` - Helper commands \
            \n\u2022 `help everyone` - Commands available to everyone'
        await channel_embed(ctx, title, desc)
        
    @help.command()
    async def admin(self, ctx):
        title = 'Admin'
        desc = '`help <command>` to get command info or give no arguments if it does not have `<help>`'
        fieldName = 'Commands:'
        fieldValue = '\
            \u2022 `reload <extension>` \
            \n\u2022 `unload <extension>` \
            \n\u2022 `load <extension>` \
            \n\u2022 `unban <user>` \
            \n\u2022 `embedcolor <default|hex color>` \
            \n\u2022 `prefix <default|prefix>` \
            \n\u2022 `<un>exempt <help|list>>` \
            \n*+ all lower commands*'
        await help_embed(ctx, title, desc, fieldValue, fieldName)

    @help.command()
    async def mod(self, ctx):
        title = 'Moderator'
        desc = '`help <command>` to get command info or give no arguments'
        fieldValue = '\
            \u2022 `ban <user> <reason>` \
            \n\u2022 `response <add|remove> <number|title> <regex> <description` \
            \n\u2022 `blacklist <add|remove>` \
            \n\u2022 `cringe <remove>` \
            \n\u2022 `kick <user> <reason>` \
            \n\u2022 `clear <number>` \
            \n\u2022 `unmute <user>` \
            \n\u2022 `nick <default|remove|name>` \
            \n\u2022 `status <default|presence>` \
            \n\u2022 `emote <name> <image attachment|image url>` \
            \n\u2022 `embed <channel|here> <title> <description>` \
            \n*+ all lower commands*'
        fieldName = 'Commands:'
        await help_embed(ctx, title, desc, fieldValue, fieldName)

    @help.command()
    async def helper(self, ctx):
        title = 'Helper'
        desc = '`help <command>` to get command info or give no arguments if it does not have `<help>`'
        fieldValue = '\
            \u2022 `mute <user> <reason>` \
            \n\u2022 `response <details|list> <number>` \
            \n\u2022 `blacklist <list>` \
            \n\u2022 `cringe <add|help>` \
            \n*+ all lower commands*'
        fieldName = 'Commands:'
        await help_embed(ctx, title, desc, fieldValue, fieldName)

    @help.command()
    async def everyone(self, ctx):
        title = 'Available to everyone:'
        desc = '`help <command>` to get command info or if it has `<help>` do `<command> help` and if it doesn\'t, giving no arguments will also give you info'
        fieldValue = '\
            \u2022 `rule<s> <number>` \
            \n\u2022 `ping <help>` \
            \n\u2022 `cringe <help>` \
            \n\u2022 `serverinfo <help>` \
            \n\u2022 `userinfo <me|user|member>` \
            \n\u2022 `<un>releases <help>` \
            \n\u2022 `<un>ignore <help>` \
            \n\u2022 `optout <I am sure>` \
            \n\u2022 `help <admin|mod|helper|everyone>`'
        fieldName = 'Commands:'
        await help_embed(ctx, title, desc, fieldValue, fieldName)
    
    ''' Help command responses '''

    @help.command()
    async def unban(self, ctx):
        title = 'Unban'
        desc = 'Unbans the specified user ID'
        fieldValue = '`unban <id>`'
        await help_embed(ctx, title, desc, fieldValue)

    @help.command()
    async def unmute(self, ctx):
        title = 'Unmute'
        desc = 'Unmutes the specified member'
        fieldValue = '`unmute <member>`'
        await help_embed(ctx, title, desc, fieldValue)

    @help.command()
    async def ban(self, ctx):
        title = 'Ban'
        desc = 'Bans the specified member'
        fieldValue = '`ban <member>`'
        await help_embed(ctx, title, desc, fieldValue)

    @help.command()
    async def mute(self, ctx):
        title = 'Mute'
        desc = 'Mutes the specified member'
        fieldValue = '`mute <member>`'
        await help_embed(ctx, title, desc, fieldValue)

    @help.command()
    async def kick(self, ctx):
        title = 'Kick'
        desc = 'Kicks the specified member'
        fieldValue = '`kick <member>`'
        await help_embed(ctx, title, desc, fieldValue)

    @help.command()
    async def blacklist(self, ctx):
        title = 'Blacklist'
        desc = 'Command to add/remove a word on the blacklist or show a list of all of the blacklisted words'
        fieldValue = '`blacklist <add|remove|list> <word>`'
        await help_embed(ctx, title, desc, fieldValue)

    @help.command()
    async def embed(self, ctx):
        title = 'Embed'
        desc = 'Sends an embed to the specified channel with the specified title/description'
        fieldValue = '`embed <channel|here> <title> <description>`'
        await help_embed(ctx, title, desc, fieldValue)

    @help.command()
    async def emote(self, ctx):
        title = 'Emote'
        desc = 'Creates an emote with the specified name and provided image'
        fieldValue = '`emote <name> <image url>` - you can attach an image instead of having a url'
        await help_embed(ctx, title, desc, fieldValue)

    @help.command()
    async def clear(self, ctx):
        title = 'Clear'
        desc = 'Clears the specified amount of messages in that channel'
        fieldValue = '`clear <number>`'
        await help_embed(ctx, title, desc, fieldValue)

    @help.command()
    async def optout(self, ctx):
        title = 'Opt-Out'
        desc = 'You will be banned from the server'
        fieldValue = '`optout <I am sure>`'
        await help_embed(ctx, title, desc, fieldValue)

    @help.command()
    async def response(self, ctx):
        title = 'Response'
        desc = 'Command to control responses, can add/remove them or list/get details of them'
        fieldValue = '`embed <add|remove|list|details> <number|title> <regex> <description>`'
        await help_embed(ctx, title, desc, fieldValue)

    @help.command()
    async def rule(self, ctx):
        title = 'Rules'
        desc = 'Sends the specified rule, or all of them'
        fieldValue = '`<rule><s> <number>`'
        await help_embed(ctx, title, desc, fieldValue)

    @help.command()
    async def prefix(self, ctx):
        title = 'Prefix'
        desc = 'Allows you to set the command prefix for the bot'
        fieldValue = '`prefix <default|new prefix>`'
        await help_embed(ctx, title, desc, fieldValue)

    @help.command()
    async def embedcolor(self, ctx):
        title = 'Embedcolor'
        desc = 'Allows you to set the embedcolor for all the embeds the bot sends'
        fieldValue = '`embedcolor <default|hex color code>`'
        await help_embed(ctx, title, desc, fieldValue)

    @help.command()
    async def nick(self, ctx):
        title = 'Nick'
        desc = 'Allows you to set the bot\'s nick in this server'
        fieldValue = '`nick <name|default|remove>`'
        await help_embed(ctx, title, desc, fieldValue)

    @help.command()
    async def status(self, ctx):
        title = 'Status'
        desc = 'Allows you to set the bot\'s status'
        fieldValue = '`status <presence|default>`'
        await help_embed(ctx, title, desc, fieldValue)

    @help.command()
    async def cringe(self, ctx):
        title = 'Cringe'
        desc = 'Either recieve a random cringe or add/remove a cringe'
        fieldValue = '`cringe <add|remove|help> <image url>` - you can attach an image instead of having a url'
        await help_embed(ctx, title, desc, fieldValue)

    @help.command()
    async def ignore(self, ctx):
        title = 'Ignored'
        desc = 'Add/remove the ignored role, if you have this role your messages will not trigger most of the regex responses'
        fieldValue = '`<un>ignore`'
        await help_embed(ctx, title, desc, fieldValue)

    @help.command()
    async def releases(self, ctx):
        title = 'Releases'
        desc = 'Add/remove the releases role, if you have this role you will be pinged when a new release comes out'
        fieldValue = '`<un>releases`'
        await help_embed(ctx, title, desc, fieldValue)

    @help.command()
    async def ping(self, ctx):
        title = 'huh'
        desc = 'why would you need help for ping? did you think it pings someone specific? xD'
        fieldValue = '`ping`'
        await help_embed(ctx, title, desc, fieldValue)

    @help.command()
    async def serverinfo(self, ctx):
        title = 'Server Information'
        desc = 'Shows information about the server'
        fieldValue = '`serverinfo`'
        await help_embed(ctx, title, desc, fieldValue)

    @help.command()
    async def userinfo(self, ctx):
        title = 'User Information'
        desc = 'Shows information about the given member/user'
        fieldValue = '`userinfo <me|user|member>`'
        await help_embed(ctx, title, desc, fieldValue)

    @help.command()
    async def load(self, ctx):
        title = ('Load')
        desc = ('Loads the specified extension')
        fieldValue = '`load <extension>`'
        await help_embed(ctx, title, desc, fieldValue)

    @help.command()
    async def unload(self, ctx):
        title = ('Unload')
        desc = ('Unloads the specified extension')
        fieldValue = '`unload <extension>`'
        await help_embed(ctx, title, desc, fieldValue)

    @help.command()
    async def reload(self, ctx):
        title = ('Reload')
        desc = ('Reloads the specified extension')
        fieldValue = '`reload <extension>`'
        await help_embed(ctx, title, desc, fieldValue)

    @help.command()
    async def exempt(self, ctx):
        title = 'Exempt'
        desc = 'Allows you to make the current channel exempted from the blacklist and regex responses, or list the current channels exempted'
        fieldValue = '`<un>exempt <list>`'
        await help_embed(ctx, title, desc, fieldValue)
    
    @help.error
    async def help_error(self, ctx, error):
        desc = None
        await error_embed(ctx, desc, error)
        logging.info(f'{ctx.author.id} tried get help but it gave the error: {error}')

def setup(bot):
    bot.add_cog(Help(bot))