import math
from pathlib import Path
import matplotlib.pyplot as plt

from Labs.Lab5.data.equation import Equation
from Labs.Lab5.data.table import Table
from Labs.Lab5.methods.interpolation import Lagrange, Gauss
from Labs.Lab5.runtime.AnyCommand import AnyCommand
from Labs.Lab5.runtime.AnyManager import AnyManager


class Lab5Command(AnyCommand):
    def __init__(self, manager: AnyManager):
        super().__init__(name="lab5", manager=manager, description="Лабораторная работа 5 (интерполяция)")

        self.funcs = [
            Equation(lambda x: x * math.sin(x ** 2), [], "x * sin(x ** 2)"),
            Equation(lambda x: math.exp(-x * x) * math.sin(x), [], "e ** (-x ** 2) * sin(x)"),
            Equation(lambda x: x * math.cos(x), [], "x * cos(x)")
        ]

        self.funcs_table = Table(head=["Номер", "Уравнение"])

        for i in range(len(self.funcs)):
            self.funcs_table.add_row([i + 1, self.funcs[i].__str__()])

    def execute(self):
        io = self.manager.get_iostream()

        n = 0
        a = 0
        b = 0
        x_train = []
        y_train = []

        mode = io.input.any_input(int,
                                  lambda m: (1 <= m <= 2, "Нужно натуральное число от 1 до 2"),
                                  "Выберите способ ввода:\n1) из файла / с клавиватуры \n2) функция")

        if mode == 1:
            file_path_str = io.input.any_input(str.strip,
                                               lambda s: (len(s) == 0 or Path(s).is_file(), "Нет такого файла"),
                                               "Введите путь файла или пустую строку (ввод с клавиатуры)")
            file_path = Path(file_path_str)

            if file_path.is_file():
                io.output.info_msg("Ввод из файла")
                io.input.from_file(file_path.resolve(False))
            else:
                io.output.info_msg("Ввод из консоли")

            n = io.input.uint_input("Введите количество точек")

            for i in range(n):
                x_train.append(io.input.float_input(f"Введите x_{i}"))
                y_train.append(io.input.float_input(f"Введите y_{i}"))

            # many y for one x

            a = x_train[0]
            b = x_train[-1]
        else:
            io.output.info_msg(self.funcs_table)
            func_num = io.input.index_input(self.funcs, 1, "Введите номер уравнения") - 1
            func = self.funcs[func_num].get_f_x()
            n = io.input.uint_input("Введите количество точек")
            a, b = io.input.interval_input("Введите рассматриваемый интервал",
                                           lambda a, b: (a != b, "Значения должны быть разные"))

            x_train = [a + (b - a) * i / (n - 1) for i in range(n)]
            y_train = [func(x) for x in x_train]

        x = io.input.float_input("Введите x")

        lagrange = Lagrange(x_train, y_train)
        gauss = Gauss(x_train, y_train)
        io.output.info_msg(f"Многочлен Лагранжа: y({x}) = {lagrange.calc(x)}\n")
        io.output.info_msg(f"Многочлен Гаусса (1-я формула): y({x}) = {gauss.calc_first(x)}")
        io.output.info_msg(f"Многочлен Гаусса (2-я формула): y({x}) = {gauss.calc_second(x)}")

        # delta_y table
        delta_y = gauss.delta_y
        head = [f"d{i + 1} y_i" for i in range(n - 1)]
        head.insert(0, "y_i")
        head.insert(0, "i")

        table = Table(head, float_digits=5)
        for i in range(n):
            row = [i - n // 2]
            for j in range(n - i):
                row.append(delta_y[j][i])
            for j in range(i):
                row.append("-")
            table.add_row(row)

        io.output.info_msg(f"Таблица конечных разностей: {table}")

        # plots

        points = 100
        x_values = [a + (b - a) * i / (points - 1) for i in range(points)]

        plt.plot(x_train, y_train, c="red", marker="o", label="исходная функция")
        plt.plot(x_values, [lagrange.calc(v) for v in x_values], c="green", label="многочлен Лагранжа")
        plt.plot(x_values, [gauss.calc_first(v) for v in x_values], c="blue", label="многочлен Гаусса (1-я формула)")
        plt.plot(x_values, [gauss.calc_second(v) for v in x_values], c="violet", label="многочлен Гаусса (2-я формула)")

        plt.legend()
        plt.show()

        io.input.from_console()
        return "Лабораторная работа 5 (интерполяция) завершилась"
