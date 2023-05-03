
class Matrix:
    def __init__(self, n=1, m=1, digits=3):
        self.rows_count = n
        self.cols_count = m
        self.digits = digits

        self.val = [0.0 for i in range(n * m)]

    def get_rows_count(self):
        return self.rows_count

    def get_cols_count(self):
        return self.cols_count

    def set_digits(self, digits):
        self.digits = digits

    def get(self, r, c):
        return self.val[r * self.cols_count + c]

    def set(self, r, c, value=0.0):
        self.val[r * self.cols_count + c] = value

    def get_row(self, r):
        return [self.get(r, i) for i in range(self.cols_count)]

    def set_row(self, r, row):
        for i in range(self.cols_count):
            self.val[r * self.cols_count + i] = row[i]

    def get_col(self, c):
        return [self.get(i, c) for i in range(self.rows_count)]

    def set_col(self, c, col):
        for i in range(self.rows_count):
            self.val[i * self.cols_count + c] = col[i]

    def swap_rows(self, r1, r2):
        temp = self.get_row(r1)
        self.set_row(r1, self.get_row(r2))
        self.set_row(r2, temp)

    def swap_cols(self, c1, c2):
        temp = self.get_col(c1)
        self.set_col(c1, self.get_col(c2))
        self.set_col(c2, temp)

    def __mul__(self, other):
        if self.get_cols_count() != other.get_rows_count():
            raise Exception(f"невозможно умножить матрицы: {self.get_rows_count()} x {self.get_cols_count()} *"
                            f" {other.get_rows_count()} x {other.get_cols_count()}")
        new_m = Matrix(self.get_rows_count(), other.get_cols_count())

        for i in range(new_m.get_rows_count()):
            for j in range(new_m.get_cols_count()):
                new_m.set(i, j, sum([(self.get(i, k) * other.get(k, j)) for k in range(new_m.get_cols_count())]))

        return new_m

    def __str__(self):
        max_len = 0
        for i in self.val:
            max_len = max(max_len, len(str(f"{i:.{self.digits}f}")))

        out = ""
        for i in range(self.rows_count):
            out += "|"

            for j in range(self.cols_count):
                this = f"{self.get(i, j):.{self.digits}f}"
                out += " " if j > 0 else ""
                out += "{}{}".format(" " * (max_len - len(this)), this)

            out += "|" + ("\n" if i < self.rows_count - 1 else "")

        return out

    def copy(self):
        new_m = Matrix(self.get_rows_count(), self.get_cols_count(), self.digits)
        new_m.val = self.val.copy()

        return new_m


def gauss_linear_solve(A: Matrix, B: Matrix):
    if A.get_rows_count() > B.get_rows_count():
        raise Exception("Размерности не подходят")

    rows = A.get_rows_count()
    cols = A.get_cols_count() + 1
    AB = Matrix(rows, cols)

    for i in range(rows):
        row = A.get_row(i)
        row.append(B.get(i, 0))
        AB.set_row(i, row)

    for i in range(rows - 1):
        max_abs = abs(AB.get(i, i))
        best_row = i
        for j in range(i + 1, rows):
            if max_abs < abs(AB.get(j, i)):
                max_abs = abs(AB.get(j, i))
                best_row = j

        if max_abs < 0.00000001:
            raise Exception("Нет однозначного решения")

        AB.swap_rows(i, best_row)

        for j in range(i + 1, rows):
            C = AB.get(j, i) / AB.get(i, i)
            AB.set(j, i, 0)

            for k in range(i + 1, cols):
                AB.set(j, k, AB.get(j, k) - C * AB.get(i, k))

    for i in range(rows - 1, -1, -1):
        for j in range(0, i):
            C = AB.get(j, i) / AB.get(i, i)
            AB.set(j, i, 0)
            AB.set(j, cols - 1, AB.get(j, cols - 1) - C * AB.get(i, cols - 1))

        AB.set(i, cols - 1, AB.get(i, cols - 1) / AB.get(i, i))
        AB.set(i, i, 1)

    return AB.get_col(cols - 1)
