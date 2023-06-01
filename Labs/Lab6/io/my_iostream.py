from Labs.Lab6.data.matrix import *
import Labs.Lab6.io.converter as converter
from Labs.Lab6.io.print_colors import ColoredPrint


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


def hard_primitive_input(converter, reader, msg, validator=lambda x: (True, "")):
    while True:
        try:
            MyOutputStream.info_msg(msg)
            s = reader()
            MyOutputStream.input_msg(s)
            result = converter(s)

            valid, validator_msg = validator(result)
            if not valid:
                raise Exception(validator_msg)

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
        file = open(file_name, "r")
        self.file_data = file.read().strip()
        file.close()
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
        if self.data_len > 0:
            if self.pointer < self.data_len:
                self.pointer = self.pointer + 1
                return self.data[self.pointer - 1]
            else:
                MyOutputStream.info_msg(f"Ввод из файла `{self.file_name}` закончен")
                self.from_console()

        return input()

    def is_from_file(self):
        return self.data_len == 0

    def any_input(self, some_converter, some_validator=lambda x: (True, ""), msg="write something"):
        return hard_primitive_input(some_converter, self.next, msg, some_validator)

    def string_input(self, msg="write string: ") -> str:
        return hard_primitive_input(str.strip, self.next, msg)

    def float_input(self, msg="write float: "):
        return hard_primitive_input(converter.str_to_float, self.next, msg)

    def uint_input(self, msg="write uint: "):
        return hard_primitive_input(converter.str_to_int, self.next, msg, validator=lambda x: (x > 0, "натуральные числа больше 0"))

    def index_input(self, array=list, offset=0, msg="write index of array: "):
        while True:
            index = self.uint_input(msg)
            if (index - offset < 0) or (index - offset >= len(array)):
                MyOutputStream.error_msg("индекс вне границ массива")
            else:
                return index

    def interval_input(self, msg="write interval: ", validator=lambda a, b: (True, "")):
        while True:
            a, b = self.float_input("первая граница интервала:"), self.float_input("вторая граница интервала")
            if a > b:
                a, b = b, a
            valid, error_msg = validator(a, b)
            if not valid:
                MyOutputStream.error_msg(error_msg)
            else:
                return a, b

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
