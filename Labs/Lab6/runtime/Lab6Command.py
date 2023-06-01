import math
from pathlib import Path
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

        self.funcs_x_y = [
            {
                "f(x,y)": Equation(lambda x, y: y + (1 + x) * y ** 2, [], "y' = y + (1 + x)y ** 2"),
                "y(x)": Equation(lambda x: 0, [], "")
            },
            {
                "f(x,y)": Equation(lambda x, y: x + y, [], "y' = x + y"),
                "y(x)": Equation(lambda x: 0, [], "")
            },
            {
                "f(x,y)": Equation(lambda x, y: x + y, [], "y' = x + y"),
                "y(x)": Equation(lambda x: 0, [], "")
            }
        ]

        self.funcs_table = Table(head=["Номер", "Уравнение"])

        for i in range(len(self.funcs_x_y)):
            self.funcs_table.add_row([i + 1, self.funcs_x_y[i]["f(x,y)"].__str__()])

    def execute(self):
        io = self.manager.get_iostream()

        io.output.info_msg(self.funcs_table)
        func_num = io.input.index_input(self.funcs_x_y, 1, "Введите номер уравнения") - 1
        func = self.funcs_x_y[func_num]["f(x,y)"].get_func()
        true_y = self.funcs_x_y[func_num]["y(x)"].get_func()

        io.output.info_msg("Ввод y(x_0) = y_0")
        x_0 = io.input.float_input("Введите x_0")
        y_0 = io.input.float_input("Введите y_0")
        x_n = io.input.any_input(converter.str_to_float, lambda v: (v > x_0, "x_n должно быть больше чем x_0"), "Введите x_n")
        h = io.input.any_input(converter.str_to_float, lambda v: ((v < x_n - x_0), "h должно быть меньше чем x_n - x_0"), "Введите шаг h")
        epsilon = io.input.float_input("Введите точность epsilon")

        euler_table, euler_y_values = euler(func, x_0, y_0, x_n, h, epsilon)
        euler_table.float_digits = 6

        runge_kutta_table, runge_kutta_y_values = runge_kutta(func, x_0, y_0, x_n, h, epsilon)
        runge_kutta_table.float_digits = 6

        milne_x_values, milne_y_values = milne(func, x_0, y_0, x_n, h, epsilon)
        milne_table = Table(head=["Номер", "x_i", "y_i", "y_точн"], float_digits=6)

        for i in range(len(milne_x_values)):
            milne_table.add_row([i, milne_x_values[i], milne_y_values[i], true_y(milne_x_values[i])])

        io.output.info_msg(f"Метод Эйлера:{euler_table}\nМетод Рунге-Кутта 4-го порядка:{runge_kutta_table}\nМетод Милна:{milne_table}")



        return "Лабораторная работа 6 (ДУ) завершилась"
