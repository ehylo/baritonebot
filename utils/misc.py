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
