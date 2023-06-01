import math
from pathlib import Path
import matplotlib.pyplot as plt

from Labs.Lab6.data.equation import Equation
from Labs.Lab6.data.table import Table
from Labs.Lab6.io import converter
from Labs.Lab6.runtime.AnyCommand import AnyCommand
from Labs.Lab6.runtime.AnyManager import AnyManager
from Labs.Lab6.methods.koshi_problem import euler


class Lab6Command(AnyCommand):
    def __init__(self, manager: AnyManager):
        super().__init__(name="lab6", manager=manager, description="Лабораторная работа 6 (ДУ)")

        self.funcs_x_y = [
            Equation(lambda x, y: y + (1 + x) * y ** 2, [], "y' = y + (1 + x)y ** 2"),
            Equation(lambda x, y: x + y, [], "y' = x + y"),
            Equation(lambda x, y: x / y, [], "y' = x / y")
        ]

        self.funcs_table = Table(head=["Номер", "Уравнение"])

        for i in range(len(self.funcs_x_y)):
            self.funcs_table.add_row([i + 1, self.funcs_x_y[i].__str__()])

    def execute(self):
        io = self.manager.get_iostream()

        io.output.info_msg(self.funcs_table)
        func_num = io.input.index_input(self.funcs_x_y, 1, "Введите номер уравнения") - 1
        func = self.funcs_x_y[func_num].get_func()

        io.output.info_msg("Ввод y(x_0) = y_0")
        x_0 = io.input.float_input("Введите x_0")
        y_0 = io.input.float_input("Введите y_0")
        x_n = io.input.any_input(converter.str_to_float, lambda v: (v > x_0, "x_n должно быть больше чем x_0"), "Введите x_n")
        h = io.input.any_input(converter.str_to_float, lambda v: (v < x_n - x_0, "h должно быть меньше чем x_n - x_0"), "Введите шаг h")
        epsilon = io.input.float_input("Введите точность epsilon")

        io.output.info_msg(euler(func, x_0, y_0, x_n, h, epsilon))

        return "Лабораторная работа 6 (ДУ) завершилась"
