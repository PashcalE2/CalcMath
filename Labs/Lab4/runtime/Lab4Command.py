from Labs.Lab4.runtime.AnyCommand import AnyCommand
from Labs.Lab4.runtime.AnyManager import AnyManager
from pathlib import Path
import Labs.Lab4.io.converter as converter
from Labs.Lab4.methods.less_squares import poly_approximation


class Lab4Command(AnyCommand):
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

        if io.input.is_from_file():
            count = io.input.uint_input("Введите количество точек")
            if count < 2 or count > 32:
                io.output.error_msg(f"Количество точек не подходит, должно быть хотя бы 8 и не больше 32")
                return "Измените входной файл так, чтобы там было необходимое количество точек"
        else:
            count = io.input.any_input(converter.str_to_int,
                               lambda n: (n >= 2 and n <= 32, "Количество точек не подходит, должно быть хотя бы 8 и не больше 32"),
                               "Введите количество точек")

        x = []
        y = []
        for i in range(count):
            x.append(io.input.float_input(f"Введите координату x точки {i + 1}"))
            y.append(io.input.float_input(f"Введите координату y точки {i + 1}"))

        print(poly_approximation(x, y, 2))

        io.input.from_console()
        return "Лабораторная работа 4 (апроксимация) завершилась"
