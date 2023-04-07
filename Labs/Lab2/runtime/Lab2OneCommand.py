from Labs.Lab2.data.equation import Equation
from Labs.Lab2.data.table import Table
from Labs.Lab2.io.my_iostream import MyInputOutputStream
from Labs.Lab2.runtime.AnyCommand import AnyCommand
from Labs.Lab2.runtime.AnyManager import AnyManager
import math
import matplotlib.pyplot as plt


def continue_search(f, x, iter, epsilon, big_f_num, big_x_num, max_iter):
    return (abs(f(x)) < big_f_num) and (abs(f(x)) > epsilon) and (iter < max_iter) and (x < big_x_num)


def lab2_interval_input(io: MyInputOutputStream):
    while True:
        try:
            a = io.input.float_input("Введите первую границу интервала:")
            b = io.input.float_input("Введите вторую границу интервала:")

            if a > b:
                a, b = b, a

            if abs(a - b) > 0.000001:
                if (abs(a) < 100) and (abs(b) < 100):
                    return a, b
                else:
                    raise Exception("Границы слишком большие: |a|, |b| < 100")
            else:
                raise Exception("Границы слишком близко: |a - b| < 0.000001")
        except Exception as e:
            io.output.error_msg(e.__str__())


def half_division_method(equation=lambda x: x, a=0.0, b=0.0, epsilon=0.001):
    result = Table(head=["Номер шага", "a", "b", "x", "f(x)"])

    x = a
    iters_count = 0
    while True:
        iters_count += 1
        x = (a + b) / 2

        result.add_row([iters_count, a, b, x, equation(x)])

        if equation(a) * equation(x) > 0:
            a = x
        else:
            b = x

        if not continue_search(equation, x, iters_count, epsilon, 1000000000, 10000, 100):
            break

    return result


def secant_method(equation=lambda x: x, x1=0.0, x2=0.0, epsilon=0.001):
    result = Table(head=["Номер шага", "x_k-1", "x_k", "x_k+1", "f(x_k+1)"])

    x3 = x1
    iters_count = 0
    while True:
        iters_count += 1

        x3 = x2 - (x2 - x1) / (equation(x2) - equation(x1)) * equation(x2)
        result.add_row([iters_count, x1, x2, x3, equation(x3)])
        x1 = x2
        x2 = x3

        if not continue_search(equation, x3, iters_count, epsilon, 1000000000, 10000, 100):
            break

    return result


def simple_iter_method(equation=lambda x: x, derivative=lambda x: x, a=0.0, b=0.0, epsilon=0.001):
    result = Table(head=["Номер шага", "x_k", "x_k+1", "f(x_k+1)"])

    lda = -1 / max([abs(derivative(a + i * (b - a) / 100)) for i in range(101)])
    phi = lambda x: x + lda * equation(x)

    x1 = b
    x2 = x1
    iters_count = 0
    while True:
        iters_count += 1
        x2 = phi(x1)
        result.add_row([iters_count, x1, x2, equation(x2)])
        x1 = x2

        if not continue_search(equation, x2, iters_count, epsilon, 1000000000, 10000, 100):
            break

    return result


class Lab2OneCommand(AnyCommand):
    def __init__(self, manager: AnyManager):
        super().__init__(name="lab2_one", manager=manager, description="Лабораторная работа 2 (нелинейное уравнение)")

        self.equations_list = [
            Equation([
                lambda x: 5 * math.cos(x) + x,
                lambda x: -5 * math.sin(x) + 1
            ], "5*cos(x) + x"),

            Equation([
                lambda x: x ** 4 + 6.64 * x ** 3 - 15.12 * x ** 2 - 55.79 * x + 63.9,
                lambda x: (4 * x ** 3 + 3 * 6.64 * x ** 2 - 2 * 15.12 * x - 55.79)
            ], "x**4 + 6.64x**3 - 15.12x**2 - 55.79x + 63.9"),

            Equation([
                lambda x: math.log((x * math.sin(x)) ** 2 + math.cos(x) ** 2 - 0.5, math.e),
                lambda x: ((x ** 2 - 1) * math.sin(2 * x) + 2 * x * math.sin(x) ** 2) /
                          ((x * math.sin(x)) ** 2 + math.cos(x) ** 2 - 0.5)
            ], "ln[(x*sin(x))**2 + cos(x)**2 - 0.5]")
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
        a, b = 0, 0

        # show plot

        x_values = [-5 + i / 10 for i in range(101)]
        y_values = [equation.derivative(0)(i) for i in x_values]

        plt.grid(visible=True)
        plt.plot(x_values, y_values)
        plt.plot(x_values, [0 for i in x_values])
        plt.show()

        # calcs

        while True:
            try:
                # enter a, b
                a, b = lab2_interval_input(io)
                io.output.info_msg(f"Рассматриваемый интервал: [{a}; {b}]")

                # check for roots
                F = []
                samples = max(100, int((b - a) * 100))

                for i in range(samples + 1):
                    F.append(equation.derivative(0)(a + i * (b - a) / samples))

                count = 0
                for i in range(len(F) - 1):
                    if F[i] * F[i + 1] < 0:
                        count += 1
                if count != 1:
                    raise Exception(f"Корней на интервале: {count} ")

                io.output.info_msg("На интервале 1 корень")
                break
            except Exception as e:
                io.output.error_msg(e.__str__())

        # now we have 1 root on [a; b], methods go

        HD_table = half_division_method(equation.derivative(0), a, b)
        io.output.info_msg(f"Метод половинного деления: {HD_table}")

        S_table = secant_method(equation.derivative(0), a, b)
        io.output.info_msg(f"Метод секущих: {S_table}")

        SI_table = simple_iter_method(equation.derivative(0), equation.derivative(1), a, b)
        io.output.info_msg(f"Метод простой итерации: {SI_table}")

        x_dots = [HD_table.get_col(3)[-1], S_table.get_col(3)[-1], SI_table.get_col(2)[-1]]
        y_dots = [HD_table.get_col(4)[-1], S_table.get_col(4)[-1], SI_table.get_col(3)[-1]]

        xlen = max(max(x_dots) - min(x_dots), 5) + 2
        a = (min(x_dots) + max(x_dots) - xlen) / 2
        b = a + xlen
        x_values = [a + i * (b - a) / 100 for i in range(101)]
        y_values = [equation.derivative(0)(i) for i in x_values]

        plt.grid(visible=True)
        plt.plot(x_values, y_values)
        plt.plot(x_values, [0 for i in x_values])

        # dots

        plt.plot([x_dots[0]], [y_dots[0]], "ro", markersize=4)
        plt.plot([x_dots[1]], [y_dots[1]], "go", markersize=4)
        plt.plot([x_dots[2]], [y_dots[2]], "bo", markersize=4)

        plt.show()

        return "Лабораторная 2 (нелинейное уравнение) завершилась"
