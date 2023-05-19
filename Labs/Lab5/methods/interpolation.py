import math


def mul(l=[]):
    result = 1.0
    for i in l:
        result = result * i
    return result


def gauss_interpolation(x_train=[], y_train=[]):
    if len(x_train) != len(y_train):
        raise Exception("Размеры данных не совпадают")

    if len(set(x_train)) != len(x_train):
        raise Exception("Несколько вариантов для одного X")

    return 0


class AnyMethod:
    name = "some name"

    def __init__(self, x_train=[], y_train=[]):
        self.x_train = x_train
        self.y_train = y_train
        self.interpolating_func = lambda x: 0

    def interpolate(self):
        pass

    def calc(self, x):
        pass

    def __str__(self):
        return self.name


class Lagrange(AnyMethod):
    name = "Метод Лагранжа"

    def __init__(self, x_train=[], y_train=[]):
        super().__init__(x_train, y_train)
        self.lagrange_elements = []
        self.interpolate()

    def interpolate(self):
        if len(self.x_train) != len(self.y_train):
            raise Exception("Размеры данных не совпадают")

        if len(set(self.x_train)) != len(self.y_train):
            raise Exception("Несколько вариантов для одного X")

        n = len(self.x_train)
        self.lagrange_elements = []

        for j in range(n):
            self.lagrange_elements.append(lambda x, i: mul([(x - x_j) / (self.x_train[i] - x_j)
                                                            for x_j in (set(self.x_train) - {self.x_train[i]})]))

        self.interpolating_func = lambda x: sum([(self.lagrange_elements[j](x, j) * self.y_train[j]) for j in range(n)])

    def calc(self, x):
        return self.interpolating_func(x)


class Gauss(AnyMethod):
    name = "Метод Гаусса"

    def __init__(self, x_train=[], y_train=[]):
        super().__init__(x_train, y_train)

        self.index_center = 0
        self.x_center = 0
        self.h = 1
        self.delta_y = []
        self.first_interpolating_func = lambda t: 0
        self.second_interpolating_func = lambda t: 0

        self.interpolate()

    def interpolate(self):
        if len(self.x_train) != len(self.y_train):
            raise Exception("Размеры данных не совпадают")

        if len(set(self.x_train)) != len(self.y_train):
            raise Exception("Несколько вариантов для одного X")

        n = len(self.x_train)

        delta_x = [self.x_train[i + 1] - self.x_train[i] for i in range(n - 1)]
        delta_x_mean = sum(delta_x) / (n - 1)
        for i in range(n - 1):
            if not (0.5 <= delta_x[i] / delta_x_mean <= 2):
                raise Exception("Промежутки между точками должны быть одинаковыми")

        self.index_center = n // 2
        self.x_center = self.x_train[self.index_center]
        self.h = delta_x_mean

        self.delta_y = [self.y_train.copy()]
        for i in range(1, n):
            self.delta_y.append([])
            for j in range(n - i):
                self.delta_y[i].append(self.delta_y[i - 1][j + 1] - self.delta_y[i - 1][j])

        self.first_interpolating_func = lambda t: self.delta_y[0][self.index_center] + sum([
            self.delta_y[i][self.index_center - i // 2] * mul([
                t + ((-1) ** j) * (j + 1) // 2
                for j in range(i)
            ]) / math.factorial(i)
            for i in range(1, len(self.x_train) - 1)
        ])

        self.second_interpolating_func = lambda t: self.delta_y[0][self.index_center] + sum([
            self.delta_y[i][self.index_center - (i + 1) // 2] * mul([
                t - ((-1) ** j) * (j + 1) // 2
                for j in range(i)
            ]) / math.factorial(i)
            for i in range(1, len(self.x_train) - 1)
        ])

    def calc_first(self, x):
        return self.first_interpolating_func((x - self.x_center) / self.h)

    def calc_second(self, x):
        return self.second_interpolating_func((x - self.x_center) / self.h)

    def calc(self, x):
        if x > self.x_center:
            return self.calc_first(x)
        return self.calc_second(x)
