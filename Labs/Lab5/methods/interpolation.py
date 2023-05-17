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
        return self.interpolating_func

    def calc(self, x):
        return self.interpolating_func(x)
