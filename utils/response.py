class Response:
    def __int__(self, title: str, description: str, regex: str, delete_message: bool, ignored_roles: list[int]):
        self.title = title
        self.description = description
        self.regex = regex
        self.delete_message = delete_message
        self.ignored_roles = ignored_roles
