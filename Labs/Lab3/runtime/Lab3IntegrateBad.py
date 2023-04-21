import math

from Labs.Lab3.data.equation import Equation
from Labs.Lab3.data.table import Table
from Labs.Lab3.runtime.AnyCommand import AnyCommand
from Labs.Lab3.runtime.AnyManager import AnyManager
from Labs.Lab3.integrals.RectanglesMethod import LeftRectanglesMethod, MiddleRectanglesMethod, RightRectanglesMethod
from Labs.Lab3.integrals.TrapezesMethod import TrapezesMethod
from Labs.Lab3.integrals.SimpsonMethod import SimpsonMethod


class Lab3IntegrateBad(AnyCommand):
    def __init__(self, manager: AnyManager):
        super().__init__(name="lab3_bad", manager=manager, description="Лабораторная работа 3, вычисление несобственного интеграла в смысле главного значения")

        self.equations_list = [
            Equation(
                lambda x: abs(math.log(abs(x), math.e)),
                [0],
                "|ln(|x|)|"
            ),

            Equation(
                lambda x: math.sin(x) / x,
                [0],
                "sin(x) / x"
            ),

            Equation(
                lambda x: 1 / ((x + 1) * (x - 2)),
                [-1, 2],
                "1 / ((x + 1) * (x - 2))"
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

        sigma = 0.000001
        a, b = io.input.interval_input("Ввод границ интервала:")

        intervals = [a]
        breaks = 0
        for point in equation.get_undef_points():
            if point == a:
                io.output.info_msg(f"Точка разрыва на левой границе: {point}")
                intervals[0] = a + sigma
                breaks += 1
            elif point == b:
                io.output.info_msg(f"Точка разрыва на правой границе: {point}")
                intervals[-1] = b - sigma
                breaks += 1
            elif (point > a) and (point < b):
                intervals.append(point - sigma)
                intervals.append(point + sigma)

                io.output.info_msg(f"Точка разрыва: {point}")
                breaks += 1

        # точка b еще не добавлена
        if abs(intervals[-1] - b) > sigma:
            intervals.append(b)

        if breaks > 0:
            io.output.info_msg(f"На интервале {breaks} точек разрыва")

        epsilon = io.input.float_input("Введите точность для правила Рунге:")

        n = 4

        io.output.info_msg("Методы для решения")
        io.output.info_msg(Table(
            head=["Номер", "Метод"],
            rows=[[i + 1, self.methods_list[i].__str__()] for i in range(len(self.methods_list))]
        ))

        method_n = io.input.index_input(self.methods_list, 1, "Введите номер метода") - 1
        method = self.methods_list[method_n]
        integrals_sum = 0
        delta = 0
        for i in range(len(intervals) // 2):
            left = intervals[2 * i]
            right = intervals[2 * i + 1]
            result = method.integrate(equation.get_f_x(), left, right, n, epsilon)
            io.output.info_msg(f"Результат работы метода на интервале: [{left}; {right}]. {method.__str__()}\n{result}")
            integrals_sum += result.get_row(-1)[2]
            delta += result.get_row(-2)[3]

        io.output.info_msg(f"Итоговое значение определенного интеграла: {integrals_sum} +- {delta}")

        return "Лабораторная работа 3, вычисление несобственного интеграла в смысле главного значения - завершена"
