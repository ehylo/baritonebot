import discord


class Responses:
    def __init__(self, bot_db, guild: discord.Guild):
        self.bot_db = bot_db
        self.guild = guild
        self.titles = bot_db.universal_response_titles[guild.id]
        self.descriptions = bot_db.universal_response_descriptions[guild.id]
        self.regexes = bot_db.universal_response_regexes[guild.id]
        self.deletes = bot_db.universal_response_deletes[guild.id]
        self.ignored_ids = bot_db.universal_response_ignored_ids[guild.id]

    def new_response(self, title, description, regex, delete, ignored_ids):
        self.titles.append(title)
        self.descriptions.append(description)
        self.regexes.append(regex)
        self.deletes.append(delete)
        self.ignored_ids.append(ignored_ids)
        self.bot_db.update_responses(self.guild, self)

    def edit_response(self, response_num_index, title, description, regex, delete, ignored_ids):
        for part, original in [
            [title, self.titles],
            [description, self.descriptions],
            [regex, self.regexes],
            [delete, self.deletes],
            [ignored_ids, self.ignored_ids]
        ]:
            if part is not None:
                original[response_num_index] = part
        self.bot_db.update_responses(self.guild, self)

    def delete_response(self, response_num_index):
        for item in [
            self.titles, self.descriptions, self.regexes, self.deletes, self.ignored_ids
        ]:
            item.pop(response_num_index)
        self.bot_db.update_responses(self.guild, self)
