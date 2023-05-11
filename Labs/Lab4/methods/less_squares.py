from Labs.Lab4.data.matrix import Matrix
from Labs.Lab4.data.matrix import gauss_linear_solve
import math


def pierson_score(x=[], y=[]):
    if len(x) != len(y):
        raise Exception("Размеры данных не совпадают")

    n = len(x)

    mean_x = sum(x) / n
    mean_y = sum(y) / n

    return sum([(x[i] - mean_x) * (y[i] - mean_y) for i in range(n)]) / (
                sum([(x[i] - mean_x) ** 2 for i in range(n)]) * sum([(y[i] - mean_y) ** 2 for i in range(n)])) ** 0.5


class AnyMethod:
    def __init__(self, x=[], y=[], name="Some method", view="y(x) = ..."):
        self.name = name
        self.view = view
        self.x = x
        self.y = y

    def set_x(self, x=[]):
        self.x = x

    def set_y(self, y=[]):
        self.y = y

    def approximation(self):
        return lambda x: 0, []


class PolyMethod(AnyMethod):
    def __init__(self, x=[], y=[], m=1):
        view = "y(x) = a_0"
        for i in range(1, m + 1):
            view += f" + a_{i} * x ** {i}"
        super().__init__(x, y, f"Полином степени {m}", view)
        self.m = m

    def approximation(self):
        if len(self.x) != len(self.y):
            raise Exception(f"Размеры данных не подходят: {len(self.x)}, {len(self.y)}")

        self.m = int(self.m)
        if self.m < 1:
            raise Exception("Степень полинома должна быть не меньше 1")

        X_sums = [sum([self.x[j] ** i for j in range(len(self.x))]) for i in range(2 * self.m + 1)]
        XY_sums = [sum([(self.x[j] ** i) * self.y[j] for j in range(len(self.x))]) for i in range(self.m + 1)]

        A = Matrix(self.m + 1, self.m + 1)
        for i in range(self.m + 1):
            A.set_row(i, [X_sums[j] for j in range(i, i + self.m + 1)])

        B = Matrix(self.m + 1, 1)
        B.set_col(0, XY_sums)
        a_numbers = gauss_linear_solve(A, B)

        return lambda t: sum([a_numbers[i] * (t ** i) for i in range(self.m + 1)]), a_numbers


class PowMethod(AnyMethod):
    def __init__(self, x=[], y=[]):
        super().__init__(x, y, "Степенная функция", "y(x) = a_0 * x ** a_1")

    def approximation(self):
        if len(self.x) != len(self.y):
            raise Exception("Размеры данных не совпадают")

        try:
            ln_x = [math.log(v, math.e) for v in self.x]
            ln_y = [math.log(v, math.e) for v in self.y]
        except Exception as e:
            raise Exception("Логарифм отрицательного числа, брух")

        func, a_numbers = PolyMethod(ln_x, ln_y, 1).approximation()
        a_numbers[0] = math.exp(a_numbers[0])

        return lambda t: a_numbers[0] * math.pow(t, a_numbers[1]), a_numbers


class ExpMethod(AnyMethod):
    def __init__(self, x=[], y=[]):
        super().__init__(x, y, "Экспонента", "y(x) = a_0 * exp(a_1 * x)")

    def approximation(self):
        if len(self.x) != len(self.y):
            raise Exception("Размеры данных не совпадают")

        try:
            ln_y = [math.log(v, math.e) for v in self.y]
        except Exception as e:
            raise Exception("Логарифм отрицательного числа, брух")

        func, a_numbers = PolyMethod(self.x, ln_y, 1).approximation()
        a_numbers[0] = math.exp(a_numbers[0])

        return lambda t: a_numbers[0] * math.exp(a_numbers[1] * t), a_numbers


class LnMethod(AnyMethod):
    def __init__(self, x=[], y=[]):
        super().__init__(x, y, "Натуральный логарифм", "y(x) = a_0 + a_1 * ln(x)")

    def approximation(self):
        if len(self.x) != len(self.y):
            raise Exception("Размеры данных не совпадают")

        try:
            ln_x = [math.log(v, math.e) for v in self.x]
        except Exception as e:
            raise Exception("Логарифм отрицательного числа, брух")

        return PolyMethod(ln_x, self.y, 1).approximation()


class LessSquares:
    def __init__(self, method: AnyMethod):
        self.method = method

    def calc(self):
        try:
            phi, a_numbers = self.method.approximation()

            deviation = [phi(self.method.x[i]) - self.method.y[i] for i in range(len(self.method.x))]
            standard_deviation = math.sqrt(sum([v ** 2 for v in deviation]) / len(self.method.x))
            r2_score = 1 - standard_deviation / (sum([phi(v ** 2) for v in self.method.x])
                                                 - sum([phi(v) ** 2 for v in self.method.x]) / len(self.method.x))

            return phi, a_numbers, deviation, standard_deviation, r2_score

        except Exception as e:
            raise Exception(f"Метод ({self.method.name}) не удалось выполнить: {e}")
