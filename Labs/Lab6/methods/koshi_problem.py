import math

from Labs.Lab6.data.table import Table


def runge_rule(y_h, y_half_h, p, epsilon):
    return abs(y_h - y_half_h) < epsilon * (2 ** p - 1)


def euler(f=lambda x, y: 0, x_0=0, y_0=0, x_n=0, h=0, epsilon=0):
    result = Table(head=["Номер шага", "y_h", "y_half_h", "R"])

    if x_0 > x_n:
        raise Exception("x_0 > x_n???")

    y_h = 0
    y_half_h = math.inf
    iterations = 0

    while not runge_rule(y_h, y_half_h, 1, epsilon):
        iterations += 1

        x = x_0
        y = y_0

        while x < x_n:
            y = y + h * f(x, y)
            x = x + h

        y_h = y_half_h
        y_half_h = y

        result.add_row([iterations, y_h, y_half_h, abs(y_h - y_half_h)])

        h /= 2

    return result


def runge_kutta():
    result = Table(head=[])

    return result


def milne():
    result = Table(head=[])

    return result
