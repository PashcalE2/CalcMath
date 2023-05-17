from pathlib import Path
import matplotlib.pyplot as plt

from Labs.Lab5.methods.interpolation import Lagrange
from Labs.Lab5.runtime.AnyCommand import AnyCommand
from Labs.Lab5.runtime.AnyManager import AnyManager


class Lab5Command(AnyCommand):
    def __init__(self, manager: AnyManager):
        super().__init__(name="lab5", manager=manager, description="Лабораторная работа 5 (интерполяция)")

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

        n = io.input.uint_input("Введите количество точек")
        x_train = []
        y_train = []

        for i in range(n):
            x_train.append(io.input.float_input(f"Введите x_{i}"))
            y_train.append(io.input.float_input(f"Введите y_{i}"))

        x = io.input.float_input("Введите x")
        lagrange = Lagrange(x_train, y_train)
        lagrange.interpolate()

        io.output.info_msg(f"Метод Лагранжа: y(x) = {lagrange.calc(x)}")

        a = x_train[0]
        b = x_train[-1]
        points = 100
        x_values = [a + (b - a) * i / (points - 1) for i in range(points)]
        plt.plot(x_values, [lagrange.calc(v) for v in x_values], c="blue")
        plt.show()

        io.input.from_console()
        return "Лабораторная работа 5 (интерполяция) завершилась"
