from Labs.Lab5.io.my_iostream import MyInputOutputStream
from Labs.Lab5.runtime.CommandManager import CommandManager


def lab4():
    iostream = MyInputOutputStream()
    app_manager = CommandManager(iostream)
    app_manager.run()


lab4()
