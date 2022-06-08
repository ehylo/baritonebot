import psycopg2

from utils.const import DATABASE_URL, DEFAULT_PRESENCE_VALUE, DEFAULT_PRESENCE_ACTION


class DB:

    def __init__(self):

        # connecting to the db
        self.db = psycopg2.connect(DATABASE_URL, sslmode='require')
        self.cur = self.db.cursor()

        self.bot_id = None
        self.presence_action = DEFAULT_PRESENCE_ACTION
        self.presence_value = DEFAULT_PRESENCE_VALUE

        # guild variables
        self.cur.execute('SELECT guild_id, prefix FROM v2guilds')
        self.prefix = dict(self.cur.fetchall())
        self.cur.execute('SELECT guild_id, embed_color FROM v2guilds')
        self.embed_color = dict([(x, int(str(y), 16)) for (x, y) in self.cur.fetchall()])
        self.cur.execute('SELECT guild_id, cringe_list FROM v2guilds')
        self.cringe_list = dict(self.cur.fetchall())
        self.cur.execute('SELECT guild_id, exempt_ids FROM v2guilds')
        self.exempted_ids = dict(self.cur.fetchall())

        # channel variables
        self.cur.execute('SELECT guild_id, logs_id FROM v2channels')
        self.logs_id = dict(self.cur.fetchall())
        self.cur.execute('SELECT guild_id, mod_logs_id FROM v2channels')
        self.mod_logs_id = dict(self.cur.fetchall())

        # role variables
        self.cur.execute('SELECT guild_id, voice_id FROM v2roles')
        self.voice_id = dict(self.cur.fetchall())
        self.cur.execute('SELECT guild_id, release_id FROM v2roles')
        self.release_id = dict(self.cur.fetchall())
        self.cur.execute('SELECT guild_id, ignore_id FROM v2roles')
        self.ignore_id = dict(self.cur.fetchall())
        self.cur.execute('SELECT guild_id, helper_ids FROM v2roles')
        self.helper_ids = dict(self.cur.fetchall())
        self.cur.execute('SELECT guild_id, mod_ids FROM v2roles')
        self.mod_ids = dict(self.cur.fetchall())
        self.cur.execute('SELECT guild_id, admin_ids FROM v2roles')
        self.admin_ids = dict(self.cur.fetchall())

        # response variables
        self.cur.execute('SELECT guild_id, title, description, regex, delete_message, ignored_roles FROM v2responses')
        self.response = dict(self.cur.fetchall())

    def update_bot_id(self, bot_id):
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

    def update_prefix(self, guild_id: int = None, prefix: str = None):
        self.cur.execute('UPDATE v2guilds SET prefix = %s WHERE guild_id = %s', (prefix, guild_id))
        self.db.commit()
        self.prefix[guild_id] = prefix

    def update_embed_color(self, guild_id: int = None, embed_color: str = None):
        self.cur.execute('UPDATE v2guilds SET embed_color = %s WHERE guild_id = %s', (embed_color, guild_id))
        self.db.commit()
        self.embed_color[guild_id] = int(str(embed_color), 16)

    def update_cringe_list(self, guild_id: int = None, cringe_list: list[str] = None):
        self.cur.execute('UPDATE v2guilds SET cringe_list = %s WHERE guild_id = %s', (cringe_list, guild_id))
        self.db.commit()
        self.cringe_list[guild_id] = cringe_list

    def update_exempted_ids(self, guild_id: int = None, exempted_ids: list[int] = None):
        self.cur.execute('UPDATE v2guilds SET exempt_ids = %s WHERE guild_id = %s', (exempted_ids, guild_id))
        self.db.commit()
        self.exempted_ids[guild_id] = exempted_ids

    def update_logs_id(self, guild_id: int = None, logs_id: int = None):
        self.cur.execute('UPDATE v2channels SET logs_id = %s WHERE guild_id = %s', (logs_id, guild_id))
        self.db.commit()
        self.logs_id[guild_id] = logs_id

    def update_mod_logs_id(self, guild_id: int = None, mod_logs_id: int = None):
        self.cur.execute('UPDATE v2channels SET mod_logs_id = %s WHERE guild_id = %s', (mod_logs_id, guild_id))
        self.db.commit()
        self.mod_logs_id[guild_id] = mod_logs_id

    def update_voice_id(self, guild_id: int = None, voice_id: int = None):
        self.cur.execute('UPDATE v2roles SET voice_id = %s WHERE guild_id = %s', (voice_id, guild_id))
        self.db.commit()
        self.voice_id[guild_id] = voice_id

    def update_release_id(self, guild_id: int = None, release_id: int = None):
        self.cur.execute('UPDATE v2roles SET release_id = %s WHERE guild_id = %s', (release_id, guild_id))
        self.db.commit()
        self.release_id[guild_id] = release_id

    def update_ignore_id(self, guild_id: int = None, ignore_id: int = None):
        self.cur.execute('UPDATE v2roles SET ignore_id = %s WHERE guild_id = %s', (ignore_id, guild_id))
        self.db.commit()
        self.ignore_id[guild_id] = ignore_id

    def update_helper_ids(self, guild_id: int = None, helper_ids: list[int] = None):
        self.cur.execute('UPDATE v2roles SET helper_ids = %s WHERE guild_id = %s', (helper_ids, guild_id))
        self.db.commit()
        self.helper_ids[guild_id] = helper_ids

    def update_mod_ids(self, guild_id: int = None, mod_ids: list[int] = None):
        self.cur.execute('UPDATE v2roles SET mod_ids = %s WHERE guild_id = %s', (mod_ids, guild_id))
        self.db.commit()
        self.mod_ids[guild_id] = mod_ids

    def update_admin_ids(self, guild_id: int = None, admin_ids: list[int] = None):
        self.cur.execute('UPDATE v2roles SET admin_ids = %s WHERE guild_id = %s', (admin_ids, guild_id))
        self.db.commit()
        self.admin_ids[guild_id] = admin_ids
