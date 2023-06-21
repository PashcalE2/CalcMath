from Labs.Lab4.io.my_iostream import MyInputOutputStream
from Labs.Lab4.runtime.CommandManager import CommandManager


def lab4():
    iostream = MyInputOutputStream()
    app_manager = CommandManager(iostream)
    app_manager.run()


lab4()
