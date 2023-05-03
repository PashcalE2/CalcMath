from Labs.Lab4.io.my_iostream import MyInputOutputStream


class AnyManager():
    def get_iostream(self) -> MyInputOutputStream:
        pass

    def get_commands(self) -> dict:
        pass

    def add_command(self, command):
        pass

    def get_command(self, name: str):
        pass

    def remove_command(self, name: str):
        pass

    def stop(self):
        pass

    def run(self):
        pass
