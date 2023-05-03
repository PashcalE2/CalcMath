from Labs.Lab4.data.matrix import Matrix
from Labs.Lab4.data.matrix import gauss_linear_solve


def pierson(xy_data=[]):
    n = len(xy_data)

    x = [p[0] for p in xy_data]
    mean_x = sum(x) / n
    y = [p[1] for p in xy_data]
    mean_y = sum(y) / n

    return sum([(x[i] - mean_x) * (y[i] - mean_y) for i in range(n)]) / (
                sum([(x[i] - mean_x) ** 2 for i in range(n)]) * sum([(y[i] - mean_y) ** 2 for i in range(n)])) ** 0.5


def poly(x=[], y=[], m=1):
    if len(x) != len(y):
        raise Exception("Размеры данных не совпадают")

    m = int(m)
    if m < 1:
        raise Exception("Степень полинома должна быть не меньше 1")

    X_sums = [sum([x[j] ** i for j in range(len(x))]) for i in range(2 * m + 1)]
    XY_sums = [sum([(x[j] ** i) * y[j] for j in range(len(x))]) for i in range(m + 1)]

    A = Matrix(m + 1, m + 1)
    for i in range(m + 1):
        A.set_row(i, [X_sums[j] for j in range(i, i + m + 1)])

    B = Matrix(m + 1, 1)
    B.set_col(0, XY_sums)

    return gauss_linear_solve(A, B)

