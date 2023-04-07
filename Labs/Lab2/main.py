from Labs.Lab2.io.my_iostream import MyInputOutputStream
from Labs.Lab2.runtime.CommandManager import CommandManager


# Вариант 13
# x ** 3 + 4.81 * x ** 2 - 17.37 * x + 5.38
# methods: 1, 4, 5, system 6
# половинное деление, секущие, простая итерация, Ньютона
def lab2():
    iostream = MyInputOutputStream()
    app_manager = CommandManager(iostream)
    app_manager.run()


lab2()
