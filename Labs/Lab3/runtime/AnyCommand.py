from Labs.Lab3.runtime.AnyManager import AnyManager


class AnyCommand:
    def __init__(self, name: str, manager: AnyManager, description: str):
        self.name = name
        self.manager = manager
        self.description = description

    def execute(self):
        return "any command result"

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description
