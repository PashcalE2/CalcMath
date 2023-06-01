from Labs.Lab6.runtime.AnyCommand import AnyCommand
from Labs.Lab6.runtime.AnyManager import AnyManager


class HelpCommand(AnyCommand):
    def __init__(self, manager: AnyManager):
        super().__init__(name="help", manager=manager, description="Вывести информацию о доступных коммандах")

    def execute(self):
        cmds = self.manager.get_commands()
        msg = "\n"

        for name in sorted(cmds):
            msg += f"{name}: {cmds[name].get_description()}\n"

        return msg
