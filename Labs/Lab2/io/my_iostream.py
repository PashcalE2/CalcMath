from Labs.Lab2.data.matrix import *
from Labs.Lab2.io.print_colors import ColoredPrint


class MyOutputStream:
    class Prefix:
        info = "Info"
        colored_info = f"{ColoredPrint.CGREEN}{info}{ColoredPrint.CEND}"

        input = "Input"
        colored_input = f"{ColoredPrint.CBLUE}{input}{ColoredPrint.CEND}"

        error = "Error"
        colored_error = f"{ColoredPrint.CRED}{error}{ColoredPrint.CEND}"

    def info_msg(*args):
        print(f"[{MyOutputStream.Prefix.colored_info}]: ", *args, sep="")
    info_msg = staticmethod(info_msg)

    def input_msg(*args):
        print(f"[{MyOutputStream.Prefix.colored_input}]: ", *args, sep="")
    input_msg = staticmethod(input_msg)

    def error_msg(*args):
        print(f"[{MyOutputStream.Prefix.colored_error}]: ", *args, sep="")
    error_msg = staticmethod(error_msg)


def str_to_float(s: str):
    try:
        return float(s.replace(",", "."))
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


def hard_primitive_input(converter, reader, msg):
    while True:
        try:
            MyOutputStream.info_msg(msg)
            s = reader()
            MyOutputStream.input_msg(s)
            result = converter(s)
            return result
        except EOFError:
            MyOutputStream.error_msg("введен символ окончания ввода - приложение заканчивает работу")
            exit(0)
        except Exception as e:
            MyOutputStream.error_msg(e.__str__())


class MyInputStream:
    def __init__(self, separator=" "):
        self.file_name = ""
        self.separator = separator
        self.file_data = ""

        self.data = []
        self.data_len = 0
        self.pointer = 0

    def from_file(self, file_name: str):
        self.file_data = open(file_name, "r").read().strip()
        self.file_name = file_name

        self.file_data = self.file_data.replace("\n", self.separator)
        self.data = self.file_data.split(self.separator)
        self.data_len = len(self.data)
        self.pointer = 0

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

    def string_input(self, msg="write string: ") -> str:
        return hard_primitive_input(str.strip, self.next, msg)

    def float_input(self, msg="write float: "):
        return hard_primitive_input(str_to_float, self.next, msg)

    def uint_input(self, msg="write uint: "):
        return hard_primitive_input(str_to_uint, self.next, msg)

    def matrix_elements_input(self, matrix: Matrix, msg="write matrix elements"):
        MyOutputStream.info_msg(msg)
        n = matrix.get_rows_count()
        m = matrix.get_cols_count()

        for i in range(n):
            for j in range(m):
                matrix.set(i, j, self.float_input(f"введите элемент [{i + 1}, {j + 1}]: "))


class MyInputOutputStream:
    def __init__(self):
        self.input = MyInputStream()
        self.output = MyOutputStream()
