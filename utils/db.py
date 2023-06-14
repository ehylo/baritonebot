import asyncpg
import discord

from utils.const import DATABASE_URL, DEFAULT_PRESENCE_VALUE, DEFAULT_PRESENCE_ACTION
from utils.responses import Responses


class DB:

    def __init__(self):
        self.db = None
        self.cur = None
        self.bot_id = None
        self.presence_action = DEFAULT_PRESENCE_ACTION
        self.presence_value = DEFAULT_PRESENCE_VALUE
        self.cringe_list = None
        self.embed_color = None
        self.exempted_ids = None
        self.mutes = None
        self.rules_titles = None
        self.rules_descriptions = None
        self.universal_response_titles = None
        self.universal_response_descriptions = None
        self.universal_response_regexes = None
        self.universal_response_deletes = None
        self.universal_response_ignored_ids = None
        self.voice_id = None
        self.release_id = None
        self.ignore_id = None
        self.muted_id = None
        self.helper_ids = None
        self.mod_ids = None
        self.admin_ids = None
        self.logs_id = None
        self.mod_logs_id = None

    async def collect_data(self):
        self.cringe_list = dict(await self.db.fetch('SELECT guild_id, cringe_list FROM v2guilds'))
        self.embed_color = dict([(x, int(str(y), 16)) for (x, y) in await self.db.fetch('SELECT guild_id, embed_color FROM v2guilds')])
        self.exempted_ids = dict(await self.db.fetch('SELECT guild_id, exempt_ids FROM v2guilds'))
        self.mutes = dict(await self.db.fetch('SELECT guild_id, mutes FROM v2guilds'))
        self.rules_titles = dict(await self.db.fetch('SELECT guild_id, rules_titles FROM v2guilds'))
        self.rules_descriptions = dict(await self.db.fetch('SELECT guild_id, rules_descriptions FROM v2guilds'))
        self.universal_response_titles = dict(await self.db.fetch('SELECT guild_id, title FROM v2responses'))
        self.universal_response_descriptions = dict(await self.db.fetch('SELECT guild_id, description FROM v2responses'))
        self.universal_response_regexes = dict(await self.db.fetch('SELECT guild_id, regex FROM v2responses'))
        self.universal_response_deletes = dict(await self.db.fetch('SELECT guild_id, delete_message FROM v2responses'))
        self.universal_response_ignored_ids = dict(await self.db.fetch('SELECT guild_id, ignored_ids FROM v2responses'))
        self.voice_id = dict(await self.db.fetch('SELECT guild_id, voice_id FROM v2constants'))
        self.release_id = dict(await self.db.fetch('SELECT guild_id, release_id FROM v2constants'))
        self.ignore_id = dict(await self.db.fetch('SELECT guild_id, ignored_id FROM v2constants'))
        self.muted_id = dict(await self.db.fetch('SELECT guild_id, muted_id FROM v2constants'))
        self.helper_ids = dict(await self.db.fetch('SELECT guild_id, helper_ids FROM v2constants'))
        self.mod_ids = dict(await self.db.fetch('SELECT guild_id, mod_ids FROM v2constants'))
        self.admin_ids = dict(await self.db.fetch('SELECT guild_id, admin_ids FROM v2constants'))
        self.logs_id = dict(await self.db.fetch('SELECT guild_id, logs_id FROM v2constants'))
        self.mod_logs_id = dict(await self.db.fetch('SELECT guild_id, mod_logs_id FROM v2constants'))

    async def connect_to_db(self):
        self.db = await asyncpg.connect(DATABASE_URL)
        await self.collect_data()

    async def update_bot_id(self, bot_id: int):
        self.bot_id = bot_id
        self.presence_action = await self.db.fetchval('SELECT presence_action FROM v2bots WHERE bot_id = $1', bot_id)
        self.presence_value = await self.db.fetchval('SELECT presence_value FROM v2bots WHERE bot_id = $1', bot_id)

    async def update_presence_action(self, presence_action: str = None):
        await self.db.execute('UPDATE v2bots SET presence_action = $1 WHERE bot_id = $2', presence_action, self.bot_id)
        self.presence_action = presence_action

    async def update_presence_value(self, presence_value: str = None):
        await self.db.execute('UPDATE v2bots SET presence_value = $1 WHERE bot_id = $2', presence_value, self.bot_id)
        self.presence_value = presence_value

    async def update_embed_color(self, guild: discord.Guild = None, embed_color: str = None):
        await self.db.execute('UPDATE v2guilds SET embed_color = $1 WHERE guild_id = $2', embed_color, guild.id)
        self.embed_color[guild.id] = int(str(embed_color), 16)

    async def update_cringe_list(self, guild: discord.Guild = None, cringe_list: list[str] = None):
        try:
            await self.db.execute('UPDATE v2guilds SET cringe_list = $1 WHERE guild_id = $2', cringe_list, guild.id)
            self.cringe_list[guild.id] = cringe_list
        except asyncpg.exceptions.InterfaceError:
            await self.connect_to_db()
            await self.db.execute('UPDATE v2guilds SET cringe_list = $1 WHERE guild_id = $2', cringe_list, guild.id)
            self.cringe_list[guild.id] = cringe_list

    async def update_exempted_ids(self, guild: discord.Guild = None, exempted_ids: list[int] = None):
        await self.db.execute('UPDATE v2guilds SET exempt_ids = $1 WHERE guild_id = $2', exempted_ids, guild.id)
        self.exempted_ids[guild.id] = exempted_ids

    async def update_mutes(self, guild: discord.Guild = None, mutes: list[int] = None):
        await self.db.execute('UPDATE v2guilds SET mutes = $1 WHERE guild_id = $2', mutes, guild.id)
        self.mutes[guild.id] = mutes

    async def update_rules_titles(self, guild: discord.Guild = None, rules_titles: list[str] = None):
        await self.db.execute('UPDATE v2guilds SET mutes = $1 WHERE guild_id = $2', rules_titles, guild.id)
        self.rules_titles[guild.id] = rules_titles

    async def update_rules_descriptions(self, guild: discord.Guild = None, rules_descriptions: list[str] = None):
        await self.db.execute('UPDATE v2guilds SET mutes = $1 WHERE guild_id = $2', rules_descriptions, guild.id)
        self.rules_descriptions[guild.id] = rules_descriptions

    async def update_responses(self, guild: discord.Guild = None, guild_responses: Responses = None):
        await self.db.execute(
            'UPDATE v2responses '
            'SET title = $1, description = $2, regex = $3, delete_message = $4, ignored_ids = $5 '
            'WHERE guild_id = $6',
            guild_responses.titles,
            guild_responses.descriptions,
            guild_responses.regexes,
            guild_responses.deletes,
            guild_responses.ignored_ids,
            guild.id
        )
        self.universal_response_titles[guild.id] = guild_responses.titles
        self.universal_response_descriptions[guild.id] = guild_responses.descriptions
        self.universal_response_regexes[guild.id] = guild_responses.regexes
        self.universal_response_deletes[guild.id] = guild_responses.deletes
        self.universal_response_ignored_ids[guild.id] = guild_responses.ignored_ids

    # unused so far
    async def update_voice_id(self, guild: discord.Guild = None, voice_id: int = None):
        await self.db.execute('UPDATE v2constants SET voice_id = $1 WHERE guild_id = $2', voice_id, guild.id)
        self.voice_id[guild.id] = voice_id

    async def update_release_id(self, guild: discord.Guild = None, release_id: int = None):
        await self.db.execute('UPDATE v2constants SET release_id = $1 WHERE guild_id = $2', release_id, guild.id)
        self.release_id[guild.id] = release_id

    async def update_ignore_id(self, guild: discord.Guild = None, ignore_id: int = None):
        await self.db.execute('UPDATE v2constants SET ignored_id = $1 WHERE guild_id = $2', ignore_id, guild.id)
        self.ignore_id[guild.id] = ignore_id

    async def update_muted_id(self, guild: discord.Guild = None, muted_id: int = None):
        await self.db.execute('UPDATE v2constants SET muted_id = $1 WHERE guild_id = $2', muted_id, guild.id)
        self.muted_id[guild.id] = muted_id

    async def update_helper_ids(self, guild: discord.Guild = None, helper_ids: list[int] = None):
        await self.db.execute('UPDATE v2constants SET helper_ids = $1 WHERE guild_id = $2', helper_ids, guild.id)
        self.helper_ids[guild.id] = helper_ids

    async def update_mod_ids(self, guild: discord.Guild = None, mod_ids: list[int] = None):
        await self.db.execute('UPDATE v2constants SET mod_ids = $1 WHERE guild_id = $2', mod_ids, guild.id)
        self.mod_ids[guild.id] = mod_ids

    async def update_admin_ids(self, guild: discord.Guild = None, admin_ids: list[int] = None):
        await self.db.execute('UPDATE v2constants SET admin_ids = $1 WHERE guild_id = $2', admin_ids, guild.id)
        self.admin_ids[guild.id] = admin_ids

    async def update_logs_id(self, guild: discord.Guild = None, logs_id: int = None):
        await self.db.execute('UPDATE v2constants SET logs_id = $1 WHERE guild_id = $2', logs_id, guild.id)
        self.logs_id[guild.id] = logs_id

    async def update_mod_logs_id(self, guild: discord.Guild = None, mod_logs_id: int = None):
        await self.db.execute('UPDATE v2constants SET mod_logs_id = $1 WHERE guild_id = $2', mod_logs_id, guild.id)
        self.mod_logs_id[guild.id] = mod_logs_id
