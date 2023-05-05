from Labs.Lab3.io.my_iostream import MyInputOutputStream
from Labs.Lab3.runtime.CommandManager import CommandManager


def lab3():
    iostream = MyInputOutputStream()
    app_manager = CommandManager(iostream)
    app_manager.run()


lab3()
