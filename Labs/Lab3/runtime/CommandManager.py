from Labs.Lab3.io.my_iostream import MyInputOutputStream
from Labs.Lab3.runtime.AnyCommand import AnyCommand
from Labs.Lab3.runtime.AnyManager import AnyManager
from Labs.Lab3.runtime.ExitCommand import ExitCommand
from Labs.Lab3.runtime.HelpCommand import HelpCommand
from Labs.Lab3.runtime.Lab3IntegrateGood import Lab3IntegrateGood
from Labs.Lab3.runtime.Lab3IntegrateBad import Lab3IntegrateBad


class CommandManager(AnyManager):
    def __init__(self, iostream: MyInputOutputStream):
        self.commands = dict()
        self.alive = False
        self.iostream = iostream

        self.add_command(ExitCommand(self))
        self.add_command(HelpCommand(self))
        self.add_command(Lab3IntegrateGood(self))
        self.add_command(Lab3IntegrateBad(self))

    def get_iostream(self):
        return self.iostream

    def get_commands(self):
        return self.commands

    def add_command(self, command: AnyCommand):
        self.commands[command.get_name()] = command

    def get_command(self, name):
        try:
            return self.commands[name]
        except KeyError as e:
            raise Exception(f"Нет такой команды '{name}'. Напишите 'help', чтобы увидеть доступные команды")

    def remove_command(self, name):
        self.commands.pop(name)

    def stop(self):
        self.alive = False

    def run(self):
        self.alive = True

        while self.alive:
            try:
                string = self.iostream.input.string_input("Введите комманду: ")
                command = self.get_command(string)
                self.iostream.output.info_msg(command.execute())
            except Exception as e:
                self.iostream.output.error_msg(e.__str__())
