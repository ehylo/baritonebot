from __future__ import annotations

import asyncpg

from database import CREATES_LIST, ALTERS_LIST
from utils import SCHEMA, DATABASE_URL


class DB:
    _db: asyncpg.connection.Connection
    _guilds: dict
    _bots: dict
    presence_action: str
    presence_value: str
    bot_id: int

    async def connect_to_db(self):

        self._db = await asyncpg.connect(DATABASE_URL)

        await self._db.execute(f'SET search_path TO {SCHEMA}')

        existing_tables = await self._db.fetch(f'SELECT table_name FROM information_schema.tables')
        existing_tables = [a['table_name'] for a in existing_tables]

        new_tables = []
        for create_table, create_query in CREATES_LIST.items():
            if create_table not in existing_tables:
                new_tables.append(create_table)
                await self._db.execute(create_query)

        for alter_table, alter_query in ALTERS_LIST.items():
            if alter_table in new_tables:
                await self._db.execute(alter_query)

        await self.collect_data()

    async def collect_data(self):

        self._bots = {}
        self._guilds = {}

        # First we need to get all rows in the database because we do a lot of reads and not many writes.
        # Start with the general bot information
        for bot_data in await self._db.fetch('SELECT * FROM bots'):
            self._bots[bot_data['bot_id']] = dict(bot_data)

        # Next we can populate the guilds dictionary with the rest of the tables
        for guild_data in await self._db.fetch('SELECT * FROM guilds'):
            guid = guild_data['guild_id']
            self._guilds[guid] = dict(guild_data)
            self._guilds[guid]['embed_color'] = int(str(self._guilds[guid]['embed_color']), 16)
            self._guilds[guid]['helper_roles'] = []
            self._guilds[guid]['mod_roles'] = []
            self._guilds[guid]['admin_roles'] = []
            self._guilds[guid]['mutes'] = []
            self._guilds[guid]['cringe_links'] = []
            self._guilds[guid]['exempt_channel_ids'] = []
            self._guilds[guid]['responses'] = {}
            self._guilds[guid]['rules'] = {}

        for helper_role_data in await self._db.fetch('SELECT * FROM helper_roles'):
            self._guilds[helper_role_data['guild_id']]['helper_roles'].append(helper_role_data['role_id'])

        for mod_role_data in await self._db.fetch('SELECT * FROM mod_roles'):
            self._guilds[mod_role_data['guild_id']]['mod_roles'].append(mod_role_data['role_id'])

        for admin_role_data in await self._db.fetch('SELECT * FROM admin_roles'):
            self._guilds[admin_role_data['guild_id']]['admin_roles'].append(admin_role_data['role_id'])

        for mute_data in await self._db.fetch('SELECT * FROM mutes'):
            mute_data = dict(mute_data)

            guid = mute_data['guild_id']
            del mute_data['guild_id']

            self._guilds[guid]['mutes'].append(mute_data)

        for cringe_link_data in await self._db.fetch('SELECT * FROM cringe_links'):
            self._guilds[cringe_link_data['guild_id']]['cringe_links'].append(cringe_link_data['url'])

        for exempt_channel_id_data in await self._db.fetch('SELECT * FROM exempt_channel_ids'):
            guid = exempt_channel_id_data['guild_id']
            self._guilds[guid]['exempt_channel_ids'].append(exempt_channel_id_data['channel_id'])

        for response_data in await self._db.fetch('SELECT * FROM responses'):
            response_data = dict(response_data)

            guid, rsp_num = response_data['guild_id'], response_data['response_id']
            del response_data['guild_id'], response_data['response_id']
            response_data['ignored_response_ids'] = []

            self._guilds[guid]['responses'][rsp_num] = response_data

        for ignored_response_id_data in await self._db.fetch('SELECT * FROM ignored_response_ids'):
            guid, rsp_num = ignored_response_id_data['guild_id'], ignored_response_id_data['response_id']

            self._guilds[guid]['responses'][rsp_num]['ignored_response_ids'].append(ignored_response_id_data['role_id'])

        for rule_data in await self._db.fetch('SELECT * FROM rules'):
            rule_data = dict(rule_data)

            guid, rule_num = rule_data['guild_id'], rule_data['rule_number']
            del rule_data['guild_id'], rule_data['rule_number']

            self._guilds[guid]['rules'][rule_num] = rule_data

    def set_bot_id(self, bot_id: int):
        self.bot_id = bot_id
        self.presence_action = self._bots[self.bot_id]['presence_action']
        self.presence_value = self._bots[self.bot_id]['presence_value']

    def get_voice_role_id(self, guild_id: int):
        return self._guilds[guild_id]['voice_role_id']

    def get_release_role_id(self, guild_id: int):
        return self._guilds[guild_id]['release_role_id']

    def get_ignored_role_id(self, guild_id: int):
        return self._guilds[guild_id]['ignored_role_id']

    def get_logs_channel_id(self, guild_id: int):
        return self._guilds[guild_id]['logs_channel_id']

    def get_mod_logs_channel_id(self, guild_id: int):
        return self._guilds[guild_id]['mod_logs_channel_id']

    def get_muted_role_id(self, guild_id: int):
        return self._guilds[guild_id]['muted_role_id']

    def get_embed_color(self, guild_id: int):
        return self._guilds[guild_id]['embed_color']

    def get_helper_role_ids(self, guild_id: int):
        return self._guilds[guild_id]['helper_roles']

    def get_mod_role_ids(self, guild_id: int):
        return self._guilds[guild_id]['mod_roles']

    def get_admin_role_ids(self, guild_id: int):
        return self._guilds[guild_id]['admin_roles']

    def get_mutes(self, guild_id: int):
        return self._guilds[guild_id]['mutes']

    def get_cringe_links(self, guild_id: int):
        return self._guilds[guild_id]['cringe_links']

    def get_exempt_channel_ids(self, guild_id: int):
        return self._guilds[guild_id]['exempt_channel_ids']

    def get_responses(self, guild_id: int):
        return self._guilds[guild_id]['responses']

    def get_rules(self, guild_id: int):
        return self._guilds[guild_id]['rules']

    async def new_response(
            self, guid: int, title: str, desc: str, regex: str, del_message: bool, ignored_response_ids: list[int]
    ):
        rid = await self._db.fetch(
            'INSERT INTO responses VALUES ($1, DEFAULT, $2, $3, $4, $5) RETURNING response_id',
            guid,
            title,
            desc,
            regex,
            del_message
        )
        rid = rid[0]['response_id']

        self._guilds[guid]['responses'][rid] = {
            'title': title,
            'description': desc,
            'regex': regex,
            'delete_message': del_message,
            'ignored_response_ids': []
        }

        for ignored_id in ignored_response_ids:
            await self._db.execute('INSERT INTO ignored_response_ids VALUES ($1, $2, $3)', guid, rid, ignored_id)
            self._guilds[guid]['responses'][rid]['ignored_response_ids'].append(ignored_id)

    async def edit_response(
            self,
            guild_id: int,
            rid: int,
            title: str = None,
            desc: str = None,
            regex: str = None,
            del_message: bool = None,
    ):
        if title:
            await self._db.execute(
                'UPDATE responses SET title = $1 WHERE guild_id = $2 AND response_id = $3', title, guild_id, rid
            )
            self._guilds[guild_id]['responses'][rid]['title'] = title

        if desc:
            await self._db.execute(
                'UPDATE responses SET description = $1 WHERE guild_id = $2 AND response_id = $3', desc, guild_id, rid
            )
            self._guilds[guild_id]['responses'][rid]['description'] = desc

        if regex:
            await self._db.execute(
                'UPDATE responses SET regex = $1 WHERE guild_id = $2 AND response_id = $3', regex, guild_id, rid
            )
            self._guilds[guild_id]['responses'][rid]['regex'] = regex

        if del_message:
            await self._db.execute(
                'UPDATE responses SET delete_message = $1 WHERE guild_id = $2 AND response_id = $3',
                del_message,
                guild_id,
                rid
            )
            self._guilds[guild_id]['responses'][rid]['delete_message'] = del_message

    async def delete_response(self, guild_id: int, rid: int):
        await self._db.execute('DELETE FROM responses WHERE guild_id = $1 AND response_id = $2', guild_id, rid)

        ignored_response_ids = self._guilds[guild_id]['responses'][rid]['ignored_response_ids']
        del self._guilds[guild_id]['responses'][rid]

        for ignored_id in ignored_response_ids:
            await self._db.execute(
                'DELETE FROM ignored_response_ids WHERE guild_id = $1 AND response_id = $2 AND role_id = $3',
                guild_id,
                rid,
                ignored_id
            )

    async def new_cringe_link(self, guild_id: int, new_url: str):
        await self._db.execute('INSERT INTO cringe_links VALUES ($1, $2)', guild_id, new_url)
        self._guilds[guild_id]['cringe_links'].append(new_url)

    async def delete_cringe_link(self, guild_id: int, url: str):
        await self._db.execute('DELETE FROM cringe_links WHERE guild_id = $1 AND url = $2', guild_id, url)
        for cringe_link in self.get_cringe_links(guild_id):
            if cringe_link['url'] == url:
                self._guilds[guild_id]['cringe_links'].remove(cringe_link)
                break

    async def edit_embed_color(self, guild_id: int, new_color: str):
        await self._db.execute('UPDATE guilds SET embed_color = $1 WHERE guild_id = $2', new_color, guild_id)
        self._guilds[guild_id]['embed_color'] = int(str(new_color), 16)

    async def delete_exempted_id(self, guild_id: int, exempted_id: int):
        await self._db.execute(
            'DELETE FROM exempt_channel_ids WHERE guild_id = $1 AND channel_id = $2', guild_id, exempted_id
        )
        for exempt_channel_id in self.get_exempt_channel_ids(guild_id):
            if exempt_channel_id['channel_id'] == exempted_id:
                self._guilds[guild_id]['exempt_channel_ids'].remove(exempt_channel_id)
                break

    async def new_exempted_id(self, guild_id: int, new_id: int):
        await self._db.execute('INSERT INTO exempt_channel_ids VALUES ($1, $2)', guild_id, new_id)
        self._guilds[guild_id]['exempt_channel_ids'].append(new_id)

    async def new_mute(self, guild_id: int, user_id: int, expiry: int):
        await self._db.execute('INSERT INTO mutes VALUES ($1, $2, $3)', guild_id, user_id, expiry)
        self._guilds[guild_id]['mutes'].append({'user_id': user_id, 'expiry': expiry})

    async def delete_mute(self, guild_id: int, user_id: int):
        await self._db.execute('DELETE FROM mutes WHERE guild_id = $1 AND user_id = $2', guild_id, user_id)
        for mute in self.get_mutes(guild_id):
            if mute['user_id'] == user_id:
                self._guilds[guild_id]['mutes'].remove(mute)
                break

    async def edit_presence_value(self, new_presence_value):
        await self._db.execute('UPDATE bots SET presence_value = $1 WHERE bot_id = $2', new_presence_value, self.bot_id)
        self._bots[self.bot_id]['presence_value'] = new_presence_value

    async def edit_presence_action(self, new_presence_action):
        await self._db.execute(
            'UPDATE bots SET presence_action = $1 WHERE bot_id = $2',
            new_presence_action,
            self.bot_id
        )
        self._bots[self.bot_id]['presence_action'] = new_presence_action
