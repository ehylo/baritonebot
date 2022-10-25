import discord


class Responses:
    def __init__(self, db, guild: discord.Guild):
        self.db = db
        self.guild = guild
        self.titles = db.universal_response_titles[guild.id]
        self.descriptions = db.universal_response_descriptions[guild.id]
        self.regexes = db.universal_response_regexes[guild.id]
        self.deletes = db.universal_response_deletes[guild.id]
        self.ignored_ids = db.universal_response_ignored_ids[guild.id]

    def new_response(self, title: str, description: str, regex: str, delete: bool, ignored_ids: str):
        self.titles.append(title)
        self.descriptions.append(description)
        self.regexes.append(regex)
        self.deletes.append(delete)
        self.ignored_ids.append(ignored_ids)
        self.db.update_responses(self.guild, self)

    def edit_response(
        self, response_num_index: int, title: str, description: str, regex: str, delete: bool, ignored_ids: str
    ):
        for part, original in [
            [title, self.titles],
            [description, self.descriptions],
            [regex, self.regexes],
            [delete, self.deletes],
            [ignored_ids, self.ignored_ids]
        ]:
            if part is not None:
                original[response_num_index] = part
        self.db.update_responses(self.guild, self)

    def delete_response(self, response_num_index: int):
        for item in [
            self.titles, self.descriptions, self.regexes, self.deletes, self.ignored_ids
        ]:
            item.pop(response_num_index)
        self.db.update_responses(self.guild, self)
