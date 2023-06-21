import math
import matplotlib.pyplot as plt

from Labs.Lab6.data.equation import Equation
from Labs.Lab6.data.table import Table
from Labs.Lab6.io import converter
from Labs.Lab6.runtime.AnyCommand import AnyCommand
from Labs.Lab6.runtime.AnyManager import AnyManager
from Labs.Lab6.methods.koshi_problem import euler, runge_kutta, milne


class Lab6Command(AnyCommand):
    def __init__(self, manager: AnyManager):
        super().__init__(name="lab6", manager=manager, description="Лабораторная работа 6 (ДУ)")

        self.funcs = [
            {
                "f(x,y)": Equation(lambda x, y: x * y / (x ** 2 + 1), [], "y' = xy / (x ** 2 + 1)"),
                "y(x,C)": Equation(lambda x, C: C * (x ** 2 + 1) ** (1/2), [], "C(x ** 2 + 1) ** (1/2)"),
                "C(x_0,y_0)": lambda x_0, y_0: y_0 / (x_0 ** 2 + 1) ** (1/2)
            },
            {
                "f(x,y)": Equation(lambda x, y: x + y, [], "y' = x + y"),
                "y(x,C)": Equation(lambda x, C: C * math.exp(x) - x - 1, [], "Ce ** x - x - 1"),
                "C(x_0,y_0)": lambda x_0, y_0: (y_0 + x_0 + 1) / math.exp(x_0)
            },
            {
                "f(x,y)": Equation(lambda x, y: y + x * y, [], "y' = y + xy"),
                "y(x,C)": Equation(lambda x, C: C * math.exp(x * (x + 2) / 2), [], "Ce ** (x(x+2)/2)"),
                "C(x_0,y_0)": lambda x_0, y_0: y_0 / math.exp(x_0 * (x_0 + 2) / 2)
            }
        ]

        self.funcs_table = Table(head=["Номер", "Уравнение"])

        for i in range(len(self.funcs)):
            self.funcs_table.add_row([i + 1, self.funcs[i]["f(x,y)"].__str__()])

    def execute(self):
        io = self.manager.get_iostream()

        io.output.info_msg(self.funcs_table)
        func_num = io.input.index_input(self.funcs, 1, "Введите номер уравнения") - 1
        func = self.funcs[func_num]["f(x,y)"].get_func()
        true_y = self.funcs[func_num]["y(x,C)"].get_func()
        C_func = self.funcs[func_num]["C(x_0,y_0)"]

        io.output.info_msg("Ввод y(x_0) = y_0")
        x_0 = io.input.float_input("Введите x_0")
        y_0 = io.input.float_input("Введите y_0")
        C = C_func(x_0, y_0)
        x_n = io.input.any_input(converter.str_to_float, lambda v: (v > x_0, "x_n должно быть больше чем x_0"), "Введите x_n")
        h = io.input.any_input(converter.str_to_float, lambda v: ((v < x_n - x_0), "h должно быть меньше чем x_n - x_0"), "Введите шаг h")
        epsilon = io.input.float_input("Введите точность epsilon")

        euler_table, euler_y_values = euler(func, x_0, y_0, x_n, h, epsilon)
        euler_table.float_digits = 6
        euler_h = euler_table.get_row(-1)[2]

        runge_kutta_table, runge_kutta_y_values = runge_kutta(func, x_0, y_0, x_n, h, epsilon)
        runge_kutta_table.float_digits = 6
        runge_kutta_h = runge_kutta_table.get_row(-1)[2]

        milne_x_values, milne_y_values = milne(func, x_0, y_0, x_n, h, epsilon)
        milne_table = Table(head=["Номер", "x_i", "y_i", "y_точн"], float_digits=6)
        milne_h = milne_x_values[1] - milne_x_values[0]

        for i in range(len(milne_x_values)):
            milne_table.add_row([i, milne_x_values[i], milne_y_values[i], true_y(milne_x_values[i], C)])

        io.output.info_msg(f"Метод Эйлера (h = {euler_h}):{euler_table}\n")
        io.output.info_msg(f"Метод Рунге-Кутта 4-го порядка (h = {runge_kutta_h}):{runge_kutta_table}\n")
        io.output.info_msg(f"Метод Милна (h = {milne_h}):{milne_table}")

        io.output.info_msg(f"Оценка погрешности метода Милна max(|y_i_точн - y_i|) = {max([abs(true_y(milne_x_values[i], C) - milne_y_values[i]) for i in range(len(milne_x_values))])}")

        plt.figure()

        min_h = min([euler_h, runge_kutta_h, milne_h])
        x_values = [x_0 + min_h * i for i in range(int((x_n - x_0) / min_h) + 1)]
        plt.plot(x_values, [true_y(x, C) for x in x_values], c="black", label="Точное решение")

        plt.plot([x_0 + euler_h * i for i in range(len(euler_y_values))], euler_y_values, c="red", label="Метод Эйлера")
        plt.plot([x_0 + runge_kutta_h * i for i in range(len(runge_kutta_y_values))], runge_kutta_y_values, c="green", label="Метод Рунге-Кутта(4го порядка)")
        plt.plot(milne_x_values, milne_y_values, c="blue", label="Метод Милна")

        plt.legend()
        plt.show()

        return "Лабораторная работа 6 (ДУ) завершилась"
