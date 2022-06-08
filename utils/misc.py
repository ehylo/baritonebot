import random

import discord


def role_hierarchy(bot_db, guild_id, enforcer, offender):

    enforcer_roles = []
    offender_roles = []

    for role in enforcer.roles:
        enforcer_roles.append(role.id)

    for role in offender.roles:
        offender_roles.append(role.id)

    for enforcer_role_id in enforcer_roles:
        if enforcer_role_id in bot_db.admin_ids[guild_id]:
            for offender_role_id in offender_roles:
                if offender_role_id in bot_db.admin_ids[guild_id]:
                    return False
            else:
                return True

    for enforcer_role_id in enforcer_roles:
        if enforcer_role_id in bot_db.mod_ids[guild_id]:
            for offender_role_id in offender_roles:
                if offender_role_id in bot_db.admin_ids[guild_id] + bot_db.mod_ids[guild_id]:
                    return False
            else:
                return True

    for enforcer_role_id in enforcer_roles:
        if enforcer_role_id in bot_db.helper_ids[guild_id]:
            for offender_role_id in offender_roles:
                staff_roles = bot_db.admin_ids[guild_id] + bot_db.mod_ids[guild_id] + bot_db.helper_ids[guild_id]
                if offender_role_id in staff_roles:
                    return False
            else:
                return True

    return True


def get_unix(discord_id):
    return int(bin(discord_id)[2:][:-22], 2) + 1420070400000


async def get_user(bot, user_id):
    return bot.get_user(user_id) if bot.get_user(user_id) is not None else await bot.fetch_user(user_id)


async def get_channel(bot, ch_id):
    return bot.get_channel(ch_id) if bot.get_channel(ch_id) is not None else await bot.fetch_channel(ch_id)


async def info_embed(bot_db, ctx, user):
    # TODO: possibly add banner and accent color but make sure that people without them are dealt with
    embed_var = discord.Embed(color=bot_db.embed_color[ctx.guild.id])
    embed_var.add_field(name='Mention:', value=user.mention)
    embed_var.add_field(
        name='Created:',
        value=user.created_at.strftime('%B %d, %Y at %I:%M:%S %p').lstrip('0').replace(' 0', ' '),
        inline=False
    )
    if ctx.guild.get_memeber(user.id) is not None:
        member = ctx.guild.get_member(user.id)
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
    embed_var.add_field(name='Default Avatar Color', value=user.default_avatar)
    embed_var.add_field(name='ID: ', value=user.id)
    embed_var.set_author(name=f'{user.name}#{user.discriminator}', icon_url=user.avatar_url)
    embed_var.set_image(url=user.avatar_url)
    embed_var.set_footer(text=f'{ctx.author.name} | ID: {ctx.author.id}', icon_url=ctx.author.avatar.url)
    return embed_var


def get_random_cringe(bot_db, ctx):
    cringe_list = bot_db.cringe_list[ctx.guild.id]
    return cringe_list[random.randint(0, len(cringe_list.length())) - 1]
