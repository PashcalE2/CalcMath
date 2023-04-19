import math

from Labs.Lab2.data.equation import Equation
from Labs.Lab2.data.table import Table
from Labs.Lab2.runtime.AnyCommand import AnyCommand
from Labs.Lab2.runtime.AnyManager import AnyManager

import matplotlib.pyplot as plt


def cramer(a11, a12, b1, a21, a22, b2):
    det_a = a11 * a22 - a12 * a21
    det_x = b1 * a22 - a12 * b2
    det_y = a11 * b2 - b1 * a21

    # print(f"(1) {a11}x + {a12}y = {b1}\n(2) {a21}x + {a22}y = {b2}\n({det_x / det_a}, {det_y / det_a})")

    return det_x / det_a, det_y / det_a


def newton_method(f, df_dx, df_dy, g, dg_dx, dg_dy, x, y, epsilon=0.01):
    result = Table(head=["Номер шага", "x_k", "y_k", "-f(x_k, y_k)", "-g(x_k, y_k)", "dx", "dy"])

    dx = 1
    dy = 1
    iters_count = 0

    # делаем пока всё не хорошо (до ответа не дошли), или пока не станет совсем плохо (улетели не пойми куда)
    while ((abs(dx) > epsilon) or (abs(dy) > epsilon)) and (abs(x) < 100) and (abs(y) < 100):
        dx, dy = cramer(
            df_dx(x, y), df_dy(x, y), -f(x, y),
            dg_dx(x, y), dg_dy(x, y), -g(x, y)
        )

        x += dx
        y += dy

        iters_count += 1
        result.add_row([iters_count, x, y, -f(x, y), -g(x, y), dx, dy])

    return result


class Lab2ManyCommand(AnyCommand):
    def __init__(self, manager: AnyManager):
        super().__init__(name="lab2_many", manager=manager, description="Лабораторная работа 2 (нелинейное уравнение)")

        self.equations_list = [
            [
                Equation([
                    lambda x, y: x**2 / 16 + y**2 / 1 - 1,
                    lambda x, y: x / 8,
                    lambda x, y: 2 * y
                ], "x**2 / 16 + y**2 / 1 - 1 = 0"),

                Equation([
                    lambda x, y: x * math.sin(x) - y,
                    lambda x, y: math.sin(x) + x * math.cos(x),
                    lambda x, y: -1,
                ], "x*sin(x) - y = 0")
            ],

            [
                Equation([
                    lambda x, y: x**2 + 2 * y - 2,
                    lambda x, y: 2 * x,
                    lambda x, y: 2
                ], "x**2 + 2 * y - 2 = 0"),

                Equation([
                    lambda x, y: x**2 / 4 + y**2 / 16 - 1,
                    lambda x, y: x / 2,
                    lambda x, y: y / 8,
                ], "x**2 / 4 + y**2 / 16 - 1 = 0")
            ],

            [
                Equation([
                    lambda x, y: x**2 + y**2 - 4,
                    lambda x, y: 2 * x,
                    lambda x, y: 2 * y
                ], "x**2 + y**2 - 4 = 0"),

                Equation([
                    lambda x, y: -3 * x ** 2 + y,
                    lambda x, y: -6 * x,
                    lambda x, y: 1
                ], "-3 * x ** 2 + y = 0")
            ]
        ]

        self.render_equations = [
            [
                Equation([lambda x: math.sqrt(1 - x**2 / 16)], ""),
                Equation([lambda x: -math.sqrt(1 - x**2 / 16)], "")
            ],
            [
                Equation([lambda x: x * math.sin(x)], "")
            ],

            [
                Equation([lambda x: 1 - x**2 / 2], "")
            ],
            [
                Equation([lambda x: 4 * math.sqrt(1 - x ** 2 / 4)], ""),
                Equation([lambda x: -4 * math.sqrt(1 - x ** 2 / 4)], "")
            ],

            [
                Equation([lambda x: math.sqrt(4 - x**2)], ""),
                Equation([lambda x: -math.sqrt(4 - x**2)], "")
            ],
            [
                Equation([lambda x: 3 * x**2], "")
            ]
        ]

    def execute(self):
        io = self.manager.get_iostream()

        io.output.info_msg("Уравнения для исследования")
        io.output.info_msg(Table(
            head=["Номер", "Система"],
            rows=[[i + 1, self.equations_list[i]] for i in range(len(self.equations_list))]
        ))

        system_n = io.input.index_input(self.equations_list, 1, "Введите номер системы:") - 1

        # show plot

        a = -5
        b = 5

        x_values = [a + i * (b - a) / 1000 for i in range(1001)]
        plot1 = []
        plot2 = []

        for eq in self.render_equations[system_n * 2]:
            y_values = []
            for x in x_values:
                try:
                    y_values.append(eq.derivative(0)(x))
                except Exception as e:
                    y_values.append(math.nan)

            plot1.append(y_values.copy())

        for eq in self.render_equations[system_n * 2 + 1]:
            y_values = []
            for x in x_values:
                try:
                    y_values.append(eq.derivative(0)(x))
                except Exception as e:
                    y_values.append(math.nan)

            plot2.append(y_values.copy())

        for y_values in plot1:
            plt.plot(x_values, y_values, color="red")
        for y_values in plot2:
            plt.plot(x_values, y_values, color="blue")
        plt.grid(visible=True)
        plt.show()

        # solve

        equations = self.equations_list[system_n]
        f = equations[0]
        g = equations[1]

        x0 = io.input.float_input("Введите начальное приближение x:")
        y0 = io.input.float_input("Введите начальное приближение y:")

        result = newton_method(
            f.derivative(0), f.derivative(1), f.derivative(2),
            g.derivative(0), g.derivative(1), g.derivative(2),
            x0, y0
        )

        io.output.info_msg(f"Метод Ньютона: {result}")

        for y_values in plot1:
            plt.plot(x_values, y_values, color="red")
        for y_values in plot2:
            plt.plot(x_values, y_values, color="blue")
        plt.plot([x0].append(result.get_col(1)), [y0].append(result.get_col(2)), "go", markersize=4)

        plt.grid(visible=True)
        plt.show()

        return "Лабораторная 2 (система функций) завершилась"
