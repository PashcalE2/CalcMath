import math

from Labs.Lab3.data.equation import Equation
from Labs.Lab3.data.table import Table
from Labs.Lab3.runtime.AnyCommand import AnyCommand
from Labs.Lab3.runtime.AnyManager import AnyManager
from Labs.Lab3.integrals.RectanglesMethod import LeftRectanglesMethod, MiddleRectanglesMethod, RightRectanglesMethod
from Labs.Lab3.integrals.TrapezesMethod import TrapezesMethod
from Labs.Lab3.integrals.SimpsonMethod import SimpsonMethod


class Lab3IntegrateGood(AnyCommand):
    def __init__(self, manager: AnyManager):
        super().__init__(name="lab3_good", manager=manager, description="Лабораторная работа 3 (вычисление собственного интеграла)")

        self.equations_list = [
            Equation(
                lambda x: 5 * math.cos(x) + x,
                [],
                "5*cos(x) + x"
            ),

            Equation(
                lambda x: x ** 4 + 6.64 * x ** 3 - 15.12 * x ** 2 - 55.79 * x + 63.9,
                [],
                "x**4 + 6.64x**3 - 15.12x**2 - 55.79x + 63.9"
            ),

            Equation(
                lambda x: math.log((x * math.sin(x)) ** 2 + math.cos(x) ** 2 - 0.5, math.e),
                [],
                "ln[(x*sin(x))**2 + cos(x)**2 - 0.5]"
            )
        ]

        self.methods_list = [
            LeftRectanglesMethod(),
            MiddleRectanglesMethod(),
            RightRectanglesMethod(),
            TrapezesMethod(),
            SimpsonMethod()
        ]

    def execute(self):
        io = self.manager.get_iostream()

        io.output.info_msg("Уравнения для исследования")
        io.output.info_msg(Table(
            head=["Номер", "Уравнение"],
            rows=[[i + 1, self.equations_list[i].__str__()] for i in range(len(self.equations_list))]
        ))

        equation_n = io.input.index_input(self.equations_list, 1, "Введите номер уравнения:") - 1
        equation = self.equations_list[equation_n]
        a, b = io.input.interval_input("Ввод границ интервала:")

        epsilon = io.input.float_input("Введите точность для правила Рунге:")

        n = 4

        io.output.info_msg("Методы для решения")
        io.output.info_msg(Table(
            head=["Номер", "Метод"],
            rows=[[i + 1, self.methods_list[i].__str__()] for i in range(len(self.methods_list))]
        ))

        method_n = io.input.index_input(self.methods_list, 1, "Введите номер метода") - 1
        method = self.methods_list[method_n]

        result = method.integrate(equation.get_f_x(), a, b, n, epsilon)
        io.output.info_msg(f"Результат работы метода. {method.__str__()}\n{result}")

        return "Лабораторная работа 3, вычисление собственного интеграла - завершена"
