from Labs.Lab4.runtime.AnyCommand import AnyCommand
from Labs.Lab4.runtime.AnyManager import AnyManager


class ExitCommand(AnyCommand):
    def __init__(self, manager: AnyManager):
        super().__init__(name="exit", manager=manager, description="Завершить работу приложения")

    def execute(self):
        self.manager.stop()
        return "Завершение работы приложения"
