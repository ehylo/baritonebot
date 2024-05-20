import random
import re

import discord


def role_hierarchy(db, guild_id: int, enforcer: discord.Member, offender: discord.Member):
    """
    A way to check if a person trying to initiate a privileged command is higher
    than the person they are taking it against to ensure proper hierarchy.

    :param db: to get the role ids from
    :param guild_id: the guild to get the role ids from
    :param enforcer: person enforcing the command
    :param offender: person who is having action taken against them
    :return: bool if the enforcer is higher or not
    """

    # no one is higher than the bot
    if offender.bot:
        return False

    enforcer_roles = []
    offender_roles = []

    # generate a list of both of their roles
    for role in enforcer.roles:
        enforcer_roles.append(role.id)

    for role in offender.roles:
        offender_roles.append(role.id)

    # check if they are an admin
    for enforcer_role_id in enforcer_roles:
        if enforcer_role_id in db.get_admin_role_ids(guild_id):
            for offender_role_id in offender_roles:
                if offender_role_id in db.get_admin_role_ids(guild_id):
                    return False
            return True

    # check if they are a mod
    for enforcer_role_id in enforcer_roles:
        if enforcer_role_id in db.get_mod_role_ids(guild_id):
            for offender_role_id in offender_roles:
                if offender_role_id in db.get_admin_role_ids(guild_id) + db.get_mod_role_ids(guild_id):
                    return False
            return True

    # check if they are a helper
    for enforcer_role_id in enforcer_roles:
        if enforcer_role_id in db.get_helper_role_ids(guild_id):
            for offender_role_id in offender_roles:
                staff_roles = db.get_admin_role_ids(guild_id)
                staff_roles += db.get_mod_role_ids(guild_id) + db.get_helper_role_ids(guild_id)
                if offender_role_id in staff_roles:
                    return False
            return True

    return True


def get_unix(discord_id: int):
    """
    Small function that uses any discord ID and gets the epoch timestamp.

    :param discord_id: The ID to convert to the epoch timestamp
    :return: the epoch timestamp
    """
    return int(bin(discord_id)[2:][:-22], 2) + 1420070400000


async def get_user(bot, user_id: int):
    """
    Tries to get the user from memory and if it isn't in memory then just make
    an api call.

    :param bot: the object to check for users
    :param user_id: user I want the object of
    :return: the user object
    """
    return bot.get_user(user_id) if bot.get_user(user_id) is not None else await bot.fetch_user(user_id)


async def get_channel(bot, ch_id: int):
    """
    Tries to get the channel from memory and if it isn't in memory then just
    make an api call.

    :param bot: the object to check for channels
    :param ch_id: channel I want the object of
    :return: the channel object
    """
    return bot.get_channel(ch_id) if bot.get_channel(ch_id) is not None else await bot.fetch_channel(ch_id)


def info_embed(db, inter: discord.Interaction, user: discord.User):
    """
    Builds an embed around the given user and information about them

    :param db: for the color
    :param inter: interaction to respond to
    :param user: the person you want information about
    :return: an embed object which contains the users information
    """
    embed_var = discord.Embed(color=db.get_embed_color(inter.guild.id))
    embed_var.add_field(name='Mention:', value=user.mention)
    embed_var.add_field(
        name='Created:',
        value=user.created_at.strftime('%B %d, %Y at %I:%M:%S %p').lstrip('0').replace(' 0', ' '),
        inline=False
    )

    # if they are a member then we can add a lot more information like roles, join date, etc.
    if inter.guild.get_member(user.id) is not None:
        member = inter.guild.get_member(user.id)
        embed_var.title = 'Member Information:'
        embed_var.add_field(
            name='Joined:',
            value=member.joined_at.strftime('%B %d, %Y at %I:%M:%S %p').lstrip('0').replace(' 0', ' '),
            inline=False
        )
        embed_var.add_field(
            name=f'Roles ({len(member.roles) - 1}):',
            value=(' '.join([str(r.mention) for r in member.roles][1:]) + '\u200b'),
            inline=False
        )
        embed_var.add_field(name='Status:', value=member.status)
    else:
        embed_var.title = 'User Information:'

    # add all the fields and return the embed
    embed_var.add_field(name='Default Avatar Color', value=user.default_avatar.key)
    embed_var.add_field(name='ID: ', value=user.id)
    embed_var.set_author(name=f'{user.name}#{user.discriminator}', icon_url=user.display_avatar.url)
    embed_var.set_image(url=user.display_avatar.url)
    embed_var.set_footer(text=f'{inter.user.name} | ID: {inter.user.id}', icon_url=inter.user.display_avatar.url)
    return embed_var


def get_random_cringe(db, inter: discord.Interaction):
    """
    Randomly chooses a cringe link from the given guilds list

    :param db: get the cringe links from
    :param inter: for which guild
    :return: url to a random cringe
    """
    cringe_list = db.get_cringe_links(inter.guild.id)
    return cringe_list[random.randint(0, len(cringe_list)) - 1]


def ignored_id_verifier(guild: discord.Guild, ignored_ids: str):
    """
    Confirms the given ignored ids

    :param guild: where the role ids should be from
    :param ignored_ids: the string of ids to check
    :return: bool if they all exist
    """
    for role_id in ignored_ids.split(' '):

        # if it isn't numeric it isn't an ID
        if not role_id.isnumeric():
            return False

        # if we can't get the role then it doesn't exist
        if guild.get_role(int(role_id)) is None:
            return False

    return True


def regex_verifier(regex: str):
    """
    Check if the given regex compiles successfully or not.

    :param regex: to be checked
    :return: bool if it is successful
    """
    if regex is None:
        return True
    try:
        re.compile(regex)
    except re.error:
        return False
    else:
        return True


def role_check(member: discord.Member, ignored_ids: list[int]):
    """
    Check if a given member has any of the ignored ids

    :param member: see if they have any ignored roles
    :param ignored_ids: the ignored role ids
    :return: bool if they do or not
    """
    for role_id in ignored_ids:
        if member.guild.get_role(role_id) in member.roles:
            return True
    return False
