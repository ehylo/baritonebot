import psycopg2
import discord

from utils.const import DATABASE_URL, DEFAULT_PRESENCE_VALUE, DEFAULT_PRESENCE_ACTION
from utils.responses import Responses


class DB:

    def __init__(self):

        # connecting to the db
        self.db = psycopg2.connect(DATABASE_URL)
        self.cur = self.db.cursor()

        self.bot_id = None
        self.presence_action = DEFAULT_PRESENCE_ACTION
        self.presence_value = DEFAULT_PRESENCE_VALUE

        self.cur.execute('SELECT guild_id, cringe_list FROM v2guilds')
        self.cringe_list = dict(self.cur.fetchall())
        self.cur.execute('SELECT guild_id, embed_color FROM v2guilds')
        self.embed_color = dict([(x, int(str(y), 16)) for (x, y) in self.cur.fetchall()])
        self.cur.execute('SELECT guild_id, exempt_ids FROM v2guilds')
        self.exempted_ids = dict(self.cur.fetchall())
        self.cur.execute('SELECT guild_id, mutes FROM v2guilds')
        self.mutes = dict(self.cur.fetchall())
        self.cur.execute('SELECT guild_id, rules_titles FROM v2guilds')
        self.rules_titles = dict(self.cur.fetchall())
        self.cur.execute('SELECT guild_id, rules_descriptions FROM v2guilds')
        self.rules_descriptions = dict(self.cur.fetchall())

        self.cur.execute('SELECT guild_id, title FROM v2responses')
        self.universal_response_titles = dict(self.cur.fetchall())
        self.cur.execute('SELECT guild_id, description FROM v2responses')
        self.universal_response_descriptions = dict(self.cur.fetchall())
        self.cur.execute('SELECT guild_id, regex FROM v2responses')
        self.universal_response_regexes = dict(self.cur.fetchall())
        self.cur.execute('SELECT guild_id, delete_message FROM v2responses')
        self.universal_response_deletes = dict(self.cur.fetchall())
        self.cur.execute('SELECT guild_id, ignored_ids FROM v2responses')
        self.universal_response_ignored_ids = dict(self.cur.fetchall())

        self.cur.execute('SELECT guild_id, voice_id FROM v2constants')
        self.voice_id = dict(self.cur.fetchall())
        self.cur.execute('SELECT guild_id, release_id FROM v2constants')
        self.release_id = dict(self.cur.fetchall())
        self.cur.execute('SELECT guild_id, ignored_id FROM v2constants')
        self.ignore_id = dict(self.cur.fetchall())
        self.cur.execute('SELECT guild_id, muted_id FROM v2constants')
        self.muted_id = dict(self.cur.fetchall())
        self.cur.execute('SELECT guild_id, helper_ids FROM v2constants')
        self.helper_ids = dict(self.cur.fetchall())
        self.cur.execute('SELECT guild_id, mod_ids FROM v2constants')
        self.mod_ids = dict(self.cur.fetchall())
        self.cur.execute('SELECT guild_id, admin_ids FROM v2constants')
        self.admin_ids = dict(self.cur.fetchall())
        self.cur.execute('SELECT guild_id, logs_id FROM v2constants')
        self.logs_id = dict(self.cur.fetchall())
        self.cur.execute('SELECT guild_id, mod_logs_id FROM v2constants')
        self.mod_logs_id = dict(self.cur.fetchall())

    def update_bot_id(self, bot_id: int):
        self.bot_id = bot_id
        self.cur.execute('SELECT presence_action FROM v2bots WHERE bot_id = %s', (bot_id, ))
        self.presence_action = self.cur.fetchone()[0]
        self.cur.execute('SELECT presence_value FROM v2bots WHERE bot_id = %s', (bot_id, ))
        self.presence_value = self.cur.fetchone()[0]

    def update_presence_action(self, presence_action: str = None):
        self.cur.execute('UPDATE v2bots SET presence_action = %s WHERE bot_id = %s', (presence_action, self.bot_id))
        self.db.commit()
        self.presence_action = presence_action

    def update_presence_value(self, presence_value: str = None):
        self.cur.execute('UPDATE v2bots SET presence_value = %s WHERE bot_id = %s', (presence_value, self.bot_id))
        self.db.commit()
        self.presence_value = presence_value

    def update_embed_color(self, guild: discord.Guild = None, embed_color: str = None):
        self.cur.execute('UPDATE v2guilds SET embed_color = %s WHERE guild_id = %s', (embed_color, guild.id))
        self.db.commit()
        self.embed_color[guild.id] = int(str(embed_color), 16)

    def update_cringe_list(self, guild: discord.Guild = None, cringe_list: list[str] = None):
        self.cur.execute('UPDATE v2guilds SET cringe_list = %s WHERE guild_id = %s', (cringe_list, guild.id))
        self.db.commit()
        self.cringe_list[guild.id] = cringe_list

    def update_exempted_ids(self, guild: discord.Guild = None, exempted_ids: list[int] = None):
        self.cur.execute('UPDATE v2guilds SET exempt_ids = %s WHERE guild_id = %s', (exempted_ids, guild.id))
        self.db.commit()
        self.exempted_ids[guild.id] = exempted_ids

    def update_mutes(self, guild: discord.Guild = None, mutes: list[int] = None):
        self.cur.execute('UPDATE v2guilds SET mutes = %s WHERE guild_id = %s', (mutes, guild.id))
        self.db.commit()
        self.mutes[guild.id] = mutes

    def update_rules_titles(self, guild: discord.Guild = None, rules_titles: list[str] = None):
        self.cur.execute('UPDATE v2guilds SET mutes = %s WHERE guild_id = %s', (rules_titles, guild.id))
        self.db.commit()
        self.rules_titles[guild.id] = rules_titles

    def update_rules_descriptions(self, guild: discord.Guild = None, rules_descriptions: list[str] = None):
        self.cur.execute('UPDATE v2guilds SET mutes = %s WHERE guild_id = %s', (rules_descriptions, guild.id))
        self.db.commit()
        self.rules_descriptions[guild.id] = rules_descriptions

    def update_responses(self, guild: discord.Guild = None, guild_responses: Responses = None):
        self.cur.execute(
            'UPDATE v2responses '
            'SET title = %s, description = %s, regex = %s, delete_message = %s, ignored_ids = %s '
            'WHERE guild_id = %s',
            (
                guild_responses.titles,
                guild_responses.descriptions,
                guild_responses.regexes,
                guild_responses.deletes,
                guild_responses.ignored_ids,
                guild.id
            )
        )
        self.db.commit()
        self.universal_response_titles[guild.id] = guild_responses.titles
        self.universal_response_descriptions[guild.id] = guild_responses.descriptions
        self.universal_response_regexes[guild.id] = guild_responses.regexes
        self.universal_response_deletes[guild.id] = guild_responses.deletes
        self.universal_response_ignored_ids[guild.id] = guild_responses.ignored_ids

    # unused so far

    def update_voice_id(self, guild: discord.Guild = None, voice_id: int = None):
        self.cur.execute('UPDATE v2constants SET voice_id = %s WHERE guild_id = %s', (voice_id, guild.id))
        self.db.commit()
        self.voice_id[guild.id] = voice_id

    def update_release_id(self, guild: discord.Guild = None, release_id: int = None):
        self.cur.execute('UPDATE v2constants SET release_id = %s WHERE guild_id = %s', (release_id, guild.id))
        self.db.commit()
        self.release_id[guild.id] = release_id

    def update_ignore_id(self, guild: discord.Guild = None, ignore_id: int = None):
        self.cur.execute('UPDATE v2constants SET ignored_id = %s WHERE guild_id = %s', (ignore_id, guild.id))
        self.db.commit()
        self.ignore_id[guild.id] = ignore_id

    def update_muted_id(self, guild: discord.Guild = None, muted_id: int = None):
        self.cur.execute('UPDATE v2constants SET muted_id = %s WHERE guild_id = %s', (muted_id, guild.id))
        self.db.commit()
        self.muted_id[guild.id] = muted_id

    def update_helper_ids(self, guild: discord.Guild = None, helper_ids: list[int] = None):
        self.cur.execute('UPDATE v2constants SET helper_ids = %s WHERE guild_id = %s', (helper_ids, guild.id))
        self.db.commit()
        self.helper_ids[guild.id] = helper_ids

    def update_mod_ids(self, guild: discord.Guild = None, mod_ids: list[int] = None):
        self.cur.execute('UPDATE v2constants SET mod_ids = %s WHERE guild_id = %s', (mod_ids, guild.id))
        self.db.commit()
        self.mod_ids[guild.id] = mod_ids

    def update_admin_ids(self, guild: discord.Guild = None, admin_ids: list[int] = None):
        self.cur.execute('UPDATE v2constants SET admin_ids = %s WHERE guild_id = %s', (admin_ids, guild.id))
        self.db.commit()
        self.admin_ids[guild.id] = admin_ids

    def update_logs_id(self, guild: discord.Guild = None, logs_id: int = None):
        self.cur.execute('UPDATE v2constants SET logs_id = %s WHERE guild_id = %s', (logs_id, guild.id))
        self.db.commit()
        self.logs_id[guild.id] = logs_id

    def update_mod_logs_id(self, guild: discord.Guild = None, mod_logs_id: int = None):
        self.cur.execute('UPDATE v2constants SET mod_logs_id = %s WHERE guild_id = %s', (mod_logs_id, guild.id))
        self.db.commit()
        self.mod_logs_id[guild.id] = mod_logs_id
