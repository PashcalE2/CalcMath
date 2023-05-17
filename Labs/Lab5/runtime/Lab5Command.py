from pathlib import Path
import matplotlib.pyplot as plt

from Labs.Lab5.runtime.AnyCommand import AnyCommand
from Labs.Lab5.runtime.AnyManager import AnyManager


class Lab5Command(AnyCommand):
    def __init__(self, manager: AnyManager):
        super().__init__(name="lab4", manager=manager, description="Лабораторная работа 4 (апроксимация)")

    def execute(self):
        io = self.manager.get_iostream()

        file_path_str = io.input.any_input(str.strip,
                                           lambda s: (len(s) == 0 or Path(s).is_file(), "Нет такого файла"),
                                           "Введите путь файла или пустую строку")
        file_path = Path(file_path_str)

        if file_path.is_file():
            io.output.info_msg("Ввод из файла")
            io.input.from_file(file_path.resolve(False))
        else:
            io.output.info_msg("Ввод из консоли")



        io.input.from_console()
        return "Лабораторная работа 5 (интерполяция) завершилась"
