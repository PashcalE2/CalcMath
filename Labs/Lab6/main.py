from Labs.Lab6.io.my_iostream import MyInputOutputStream
from Labs.Lab6.runtime.CommandManager import CommandManager


def lab6():
    iostream = MyInputOutputStream()
    app_manager = CommandManager(iostream)
    app_manager.run()


lab6()
