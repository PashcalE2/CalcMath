import math

from Labs.Lab6.data.table import Table


def runge_rule(y_h, y_half_h, p, epsilon):
    return abs(y_h - y_half_h) < epsilon * (2 ** p - 1)


def euler(f=lambda x, y: 0, x_0=0, y_0=0, x_n=0, h=0, epsilon=0):
    result = Table(head=["Номер шага", "h", "half_h", "y_h", "y_half_h", "R"])

    if x_0 > x_n:
        raise Exception("x_0 > x_n???")

    y_h = 0
    y_half_h = math.inf
    iterations = 0
    y_values = []

    while not runge_rule(y_h, y_half_h, 1, epsilon):
        iterations += 1

        x = x_0
        y = y_0

        y_values = [y]

        while x < x_n:
            y = y + h * f(x, y)
            x = x + h

            y_values.append(y)

        y_h = y_half_h
        y_half_h = y

        result.add_row([iterations, h * 2, h, y_h, y_half_h, abs(y_h - y_half_h)])

        h /= 2

    return result, y_values


def runge_kutta(f=lambda x, y: 0, x_0=0, y_0=0, x_n=0, h=0, epsilon=0):
    result = Table(head=["Номер шага", "h", "half_h", "y_h", "y_half_h", "R"])

    if x_0 > x_n:
        raise Exception("x_0 > x_n???")

    y_h = 0
    y_half_h = math.inf
    iterations = 0
    y_values = []

    while not runge_rule(y_h, y_half_h, 4, epsilon):
        iterations += 1

        x = x_0
        y = y_0
        y_values = [y]

        while x < x_n:
            k1 = h * f(x, y)
            k2 = h * f(x + h / 2, y + k1 / 2)
            k3 = h * f(x + h / 2, y + k2 / 2)
            k4 = h * f(x + h, y + k3)
            y = y + 1 / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
            x = x + h

            y_values.append(y)

        y_h = y_half_h
        y_half_h = y

        result.add_row([iterations, h * 2, h, y_h, y_half_h, abs(y_h - y_half_h) / 15])

        h /= 2

    return result, y_values


def milne(f=lambda x, y: 0, x_0=0, y_0=0, x_n=0, h=0, epsilon=0):
    if x_0 > x_n:
        raise Exception("x_0 > x_n???")

    runge_kutta_table, y_values = runge_kutta(f, x_0, y_0, x_n, h, epsilon)
    h = runge_kutta_table.get_row(-1)[2]
    x_values = [(x_0 + i * h) for i in range(3)]
    y_values = y_values[:3]
    x = x_values[-1] + h

    while x < x_n:
        y_suggestion = y_values[-3] + 4 * h / 3 * (2 * f(x_values[-3], y_values[-3]) - f(x_values[-2], y_values[-2]) + 2 * f(x_values[-1], y_values[-1]))
        y_corrected = y_values[-2] + h / 3 * (f(x_values[-2], y_values[-2]) + 4 * f(x_values[-1], y_values[-1]) + f(x, y_suggestion))

        while abs(y_suggestion - y_corrected) > epsilon:
            y_corrected = y_values[-2] + h / 3 * (f(x_values[-2], y_values[-2]) + 4 * f(x_values[-1], y_values[-1]) + f(x, y_corrected))

        x_values.append(x)
        y_values.append(y_corrected)

        x += h

    return x_values, y_values
