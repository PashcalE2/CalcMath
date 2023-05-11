import math
from pathlib import Path
import matplotlib.pyplot as plt

import Labs.Lab4.io.converter as converter
from Labs.Lab4.data.table import Table
from Labs.Lab4.methods.less_squares import PolyMethod, ExpMethod, PowMethod, LnMethod, LessSquares, pierson_score
from Labs.Lab4.runtime.AnyCommand import AnyCommand
from Labs.Lab4.runtime.AnyManager import AnyManager


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
            if count < 8 or count > 32:
                io.output.error_msg(f"Количество точек не подходит, должно быть хотя бы 8 и не больше 32")
                return "Измените входной файл так, чтобы там было необходимое количество точек"
        else:
            count = io.input.any_input(converter.str_to_int,
                               lambda n: (n >= 8 and n <= 32, "Количество точек не подходит, должно быть хотя бы 8 и не больше 32"),
                               "Введите количество точек")

        x = []
        y = []
        for i in range(count):
            x.append(io.input.float_input(f"Введите координату x точки {i + 1}"))
            y.append(io.input.float_input(f"Введите координату y точки {i + 1}"))

        # less squares

        all_methods = [PolyMethod(x, y, 1), PolyMethod(x, y, 2), PolyMethod(x, y, 3),
                       PowMethod(x, y), ExpMethod(x, y), LnMethod(x, y)]

        best_phi = lambda t: 0
        best_a_numbers = []
        best_deviation = []
        best_standard_deviation = 0
        best_r2_score = 0
        best_method_name = "none"
        best_method_view = "none"

        for method in all_methods:
            try:
                phi, a_numbers, deviation, standard_deviation, r2_score = LessSquares(method).calc()

                if abs(best_r2_score - 1) > abs(r2_score - 1):
                    best_phi = phi
                    best_a_numbers = a_numbers
                    best_deviation = deviation
                    best_standard_deviation = standard_deviation
                    best_r2_score = r2_score
                    best_method_name = method.name
                    best_method_view = method.view
            except Exception as e:
                io.output.error_msg(e)

        io.output.info_msg(f"Лучшая функция: {best_method_view}")

        s = ""
        for i in range(len(best_a_numbers)):
            s += f"a_{i} = {best_a_numbers[i]}\n"
        io.output.info_msg(f"Коэффициенты аппроксимирующей функции:\n{s}")

        table = Table(head=["x_i", "y_i", "phi_i", "epsilon_i"])
        for i in range(len(x)):
            table.add_row([x[i], y[i], best_phi(x[i]), best_deviation[i]])

        io.output.info_msg(table)
        io.output.info_msg(f"Среднеквадратическое отклонение: {best_standard_deviation}")

        if best_method_name == all_methods[0].name:
            io.output.info_msg(f"Коэффициент корелляции Пирсона: {pierson_score(x, y)}")

        io.output.info_msg(f"R ** 2 = {best_r2_score}")

        # plots
        a = min(x)
        b = max(x)
        plot_points_count = 100
        plot_x = [a + (b - a) * (i - 3) / (plot_points_count - 7) for i in range(plot_points_count)]

        plt.figure()
        plt.scatter(x, y, c="black")
        plt.plot(plot_x, [best_phi(t) for t in plot_x], label=best_method_name)
        plt.legend()
        plt.show()

        io.input.from_console()
        return "Лабораторная работа 4 (апроксимация) завершилась"
