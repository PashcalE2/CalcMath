
def str_justify_left(s="", n=0, char=" "):
    if len(s) >= n:
        return s

    if len(s) == 0:
        return char * n

    right = (n - len(s))

    return s + char * right


def str_justify_center(s="", n=0, char=" "):
    if len(s) >= n:
        return s

    if len(s) == 0:
        return char * n

    left = (n - len(s)) // 2
    right = n - (left + len(s))

    return char * left + s + char * right


def str_justify_right(s="", n=0, char=" "):
    if len(s) >= n:
        return s

    if len(s) == 0:
        return char * n

    left = (n - len(s))

    return char * left + s


def list_justify_center(arr=[], n=0, element=[]):
    if len(arr) >= n:
        return arr

    if len(arr) == 0:
        return [element for i in range(n)]

    left = (n - len(arr)) // 2
    right = n - (left + len(arr))

    for i in range(left):
        arr.insert(0, element)

    for i in range(right):
        arr.append(element)

    return arr


class Table:
    def __init__(self, head=[], rows=[], float_digits=3):
        self.rows = rows.copy()
        self.rows.insert(0, head.copy())

        self.head = self.rows[0]
        self.float_digits = float_digits

    def get_head(self):
        return self.head

    def set_head(self, head=[]):
        self.head = head.copy()

    def add_row(self, row=[]):
        if len(row) != len(self.head):
            raise Exception("количество элементов не совпадает")
        self.rows.append(row)

    def get_row(self, row_id=0):
        if row_id < -len(self.head) or row_id > len(self.head):
            raise Exception("индекс вне границ")

        return self.rows[row_id]

    def set_row(self, row_id=0, row=[]):
        if len(row) != len(self.head):
            raise Exception("количество элементов не совпадает")

        if row_id < 1 or row_id > len(self.head):
            raise Exception("индекс вне границ")

        self.rows[row_id] = row.copy()

    def get_col(self, col_id=0):
        if (col_id < 0) or (col_id > len(self.rows[0])):
            raise Exception("индекс вне границ")

        return [self.rows[i + 1][col_id] for i in range(len(self.rows) - 1)]

    def set_cell(self, row_id=0, col_id=0, value=""):
        self.rows[row_id][col_id] = value

    def get_cell(self, row_id=0, col_id=0):
        return self.rows[row_id][col_id]

    def get_rows_count(self):
        return len(self.rows)

    def __str__(self):
        str_rows = []
        rows_height = [0 for i in range(len(self.rows))]
        cols_width = [0 for i in range(len(self.head))]
        padding = 1

        # forming string data
        for row in self.rows:
            str_row = []
            str_rows.append(str_row)

            for data in row:
                str_data = str(data)
                if type(data) == float:
                    str_data = f"{data:.{self.float_digits}f}"
                if type(data) == list:
                    str_data = ""
                    for el in data:
                        str_data += str(el) + "\n"
                str_row.append(str_data.strip().split("\n"))

        # calculating max width and height
        for i in range(len(str_rows)):
            for j in range(len(str_rows[i])):
                rows_height[i] = max(rows_height[i], len(str_rows[i][j]))
                for str_data in str_rows[i][j]:
                    cols_width[j] = max(cols_width[j], len(str_data))

        # justify center
        for i in range(len(str_rows)):
            for j in range(len(str_rows[0])):
                str_rows[i][j] = list_justify_center(str_rows[i][j], rows_height[i], [])
                for k in range(len(str_rows[i][j])):
                    str_rows[i][j][k] = str_justify_center(str_justify_right(str_rows[i][j][k], cols_width[j]), cols_width[j] + padding * 2)

        result = "\n"
        width_char = "-"
        height_char = "|"
        cross_char = "+"

        break_line = "" + cross_char
        for i in range(len(cols_width)):
            break_line += width_char * (cols_width[i] + padding * 2) + cross_char
        break_line += "\n"

        result += break_line
        for i in range(len(str_rows)):
            for k in range(len(str_rows[i][0])):
                result += height_char
                for j in range(len(str_rows[0])):
                    result += str_rows[i][j][k] + height_char
                result += "\n"
            result += break_line

        return result
