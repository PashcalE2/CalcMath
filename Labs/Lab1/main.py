
def print_info(*args):
    print("[Info]", *args)


def print_input(*args):
    print("[Input]", *args)


def print_err(*args):
    print("[Error]", *args)


def hard_primitive_input(converter, reader, msg):
    while True:
        try:
            print_info(msg)
            s = reader()
            print_input(s)
            result = converter(s)
            return result
        except Exception as e:
            print_err(e.__str__())


def str_to_float(s: str):
    try:
        return float(s)
    except ValueError:
        raise Exception("неверный формат числа с плавающей точкой")


def str_to_uint(s: str):
    try:
        n = int(s)
        if n <= 0:
            raise ValueError

        return n
    except ValueError:
        raise Exception("неверный формат натурального числа")


class Matrix:
    def __init__(self, n=1, m=1, digits=3):
        self.rows_count = n
        self.cols_count = m
        self.digits = digits

        self.val = [0 for i in range(n * m)]

    def get_rows_count(self):
        return self.rows_count

    def get_cols_count(self):
        return self.cols_count

    def set_digits(self, digits):
        self.digits = digits

    def get(self, r, c):
        return self.val[r * self.cols_count + c]

    def set(self, r, c, value=0):
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


class MyInputStream:
    def __init__(self, separator=" "):
        self.file_name = ""
        self.separator = separator
        self.file_data = ""

        self.data = []
        self.data_len = 0
        self.pointer = 0

    def from_file(self, file_name: str):
        try:
            self.file_data = open(file_name, "r").read().strip()
            self.file_name = file_name

            self.file_data = self.file_data.replace("\n", self.separator)
            self.data = self.file_data.split(self.separator)
            self.data_len = len(self.data)
            self.pointer = 0
        except Exception as e:
            print(f"[Error] >> {e}")

    def from_console(self):
        self.file_name = ""
        self.file_data = ""

        self.data = []
        self.data_len = 0
        self.pointer = 0

    def next(self):
        if self.pointer < self.data_len:
            self.pointer = self.pointer + 1
            return self.data[self.pointer - 1]

        return input()

    def string_input(self, msg="write string: "):
        return hard_primitive_input(str.strip, self.next, msg)

    def float_input(self, msg="write float: "):
        return hard_primitive_input(str_to_float, self.next, msg)

    def uint_input(self, msg="write uint: "):
        return hard_primitive_input(str_to_uint, self.next, msg)

    def matrix_elements_input(self, matrix: Matrix, msg="write matrix elements"):
        print_info(msg)
        n = matrix.get_rows_count()
        m = matrix.get_cols_count()

        for i in range(n):
            for j in range(m):
                matrix.set(i, j, self.float_input(f"введите элемент [{i + 1}, {j + 1}]: "))


def lab1():
    s = MyInputStream(" ")

    file_name = s.string_input("введите имя файла: ")
    s.from_file(file_name)

    matrix = Matrix(s.uint_input("введите количество строк:"), s.uint_input("введите количество столбцов:"))
    if matrix.get_rows_count() != matrix.get_cols_count():
        print_err("матрица не квадратная")
        exit()

    s.matrix_elements_input(matrix, "ввод элементов матрицы A")
    if (matrix.get_rows_count() > 20) | (matrix.get_cols_count() > 20):
        print_err("слишком большая размерность (> 20)")
        exit()

    print_info(f"введенная матрица:\n{matrix}")

    b_vector = Matrix(1, matrix.get_rows_count())
    s.matrix_elements_input(b_vector, "ввод элементов вектора B")

    epsilon = s.float_input("ввод эпсилон")

    def gauss_zeydel(input_m: Matrix, b: list, epsilon=0.001):
        m = input_m.copy()
        rows = m.get_rows_count()
        cols = m.get_cols_count()
        if rows != cols:
            raise Exception("матрица не квадратная")
        if len(b) < rows:
            raise Exception("размерность вектора B не подходит")

        # приведение к диагональному преобладанию
        for i in range(rows - 1):
            max_el_abs = abs(m.get(i, i))
            best_row = i
            for j in range(i + 1, rows):
                if abs(m.get(j, i)) > max_el_abs:
                    max_el_abs = abs(m.get(j, i))
                    best_row = j

            if i != best_row:
                m.swap_rows(i, best_row)

                temp = b[i]
                b[i] = b[best_row]
                b[best_row] = temp

                # print(i, best_row)

            if max_el_abs < 0.0000000001:
                raise Exception("нулевой столбец")

        strong_diagonal = True
        for i in range(rows):
            row_sum = sum([abs(m.get(i, j)) for j in range(rows)]) - abs(m.get(i, i))
            if abs(m.get(i, i)) < row_sum:
                strong_diagonal = False
                break

        if strong_diagonal:
            print_info("диагональное преобладание **присутствует**")
        else:
            print_info("диагональное преобладание **отсутствует**")

        for i in range(rows):
            el = m.get(i, i)
            m.set_row(i, [(j / el) for j in m.get_row(i)])
            b[i] = b[i] / el

            m.set(i, i, 0)

        x1 = b.copy()
        running = True
        c = 0
        while running:
            x0 = x1.copy()
            for i in range(rows):
                x1[i] = b[i]
                for j in range(i):
                    x1[i] -= m.get(i, j) * x1[j]
                for j in range(i + 1, rows):
                    x1[i] -= m.get(i, j) * x0[j]

            c += 1
            # print_info(f"iter = {c}\nx0 = {x0}\nx1 = {x1}")

            for i in range(rows):
                running = running and (abs(x1[i] - x0[i]) <= epsilon)
            running = not running

        return x1, [abs(x1[i] - x0[i]) for i in range(rows)]

    x = Matrix(1, matrix.get_rows_count(), 9)

    x_ans, errors = gauss_zeydel(matrix, b_vector.get_row(0), epsilon)
    x.set_row(0, x_ans)

    print_info(f"Ответ: x = {x}. Вектор погрешностей: {errors}")
    print_info("Проверка.\n", f"Ax = {x * matrix}\n", f"B = {b_vector}")


lab1()