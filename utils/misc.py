import random
import re

import discord


def role_hierarchy(db, guild_id: int, enforcer: discord.Member, offender: discord.Member):

    if offender.bot:
        return False

    enforcer_roles = []
    offender_roles = []

    for role in enforcer.roles:
        enforcer_roles.append(role.id)

    for role in offender.roles:
        offender_roles.append(role.id)

    for enforcer_role_id in enforcer_roles:
        if enforcer_role_id in db.get_admin_role_ids(guild_id):
            for offender_role_id in offender_roles:
                if offender_role_id in db.get_admin_role_ids(guild_id):
                    return False
            return True

    for enforcer_role_id in enforcer_roles:
        if enforcer_role_id in db.get_mod_role_ids(guild_id):
            for offender_role_id in offender_roles:
                if offender_role_id in db.get_admin_role_ids(guild_id) + db.get_mod_role_ids(guild_id):
                    return False
            return True

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
    return int(bin(discord_id)[2:][:-22], 2) + 1420070400000


async def get_user(bot, user_id: int):
    return bot.get_user(user_id) if bot.get_user(user_id) is not None else await bot.fetch_user(user_id)


async def get_channel(bot, ch_id: int):
    return bot.get_channel(ch_id) if bot.get_channel(ch_id) is not None else await bot.fetch_channel(ch_id)


def info_embed(db, inter: discord.Interaction, user: discord.User):
    embed_var = discord.Embed(color=db.get_embed_color(inter.guild.id))
    embed_var.add_field(name='Mention:', value=user.mention)
    embed_var.add_field(
        name='Created:',
        value=user.created_at.strftime('%B %d, %Y at %I:%M:%S %p').lstrip('0').replace(' 0', ' '),
        inline=False
    )
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
    embed_var.add_field(name='Default Avatar Color', value=user.default_avatar.key)
    embed_var.add_field(name='ID: ', value=user.id)
    embed_var.set_author(name=f'{user.name}#{user.discriminator}', icon_url=user.display_avatar.url)
    embed_var.set_image(url=user.display_avatar.url)
    embed_var.set_footer(text=f'{inter.user.name} | ID: {inter.user.id}', icon_url=inter.user.display_avatar.url)
    return embed_var


def get_random_cringe(db, inter: discord.Interaction):
    cringe_list = db.get_cringe_links(inter.guild.id)
    return cringe_list[random.randint(0, len(cringe_list)) - 1]


def ignored_id_verifier(guild: discord.Guild, ignored_ids: str):
    for role_id in ignored_ids.split(' '):
        if not role_id.isnumeric():
            return False
        if guild.get_role(int(role_id)) is None:
            return False
    return True


def regex_verifier(regex: str):
    if regex is None:
        return True
    try:
        re.compile(regex)
    except re.error:
        return False
    else:
        return True


def role_check(member: discord.Member, ignored_ids: list[int]):
    for role_id in ignored_ids:
        if member.guild.get_role(role_id) in member.roles:
            return True
