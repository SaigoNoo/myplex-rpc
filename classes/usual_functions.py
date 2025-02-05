from json import load, dumps

"""
Here will be stored different tools who will help to get some common values or operation
"""


class File:
    def __init__(self, file: str):
        self.file = file
        self.data = None

    def get_value(self, key: str):
        self.update_data()
        return self.data[key] if self.key_exist(key=key) else False

    def update_data(self):
        with open(file=self.file, mode="r", encoding="utf-8") as config:
            self.data = load(config)

    def set_value(self, key: str, value: str or list, create_file: bool = False):
        with open(file=self.file, mode="w", encoding="utf-8") as config:
            if create_file:
                self.data = {key: value}
            else:
                self.update_data()
                self.data[key] = value
            config.write(dumps(self.data, indent=2))

    def write_to_file(self, data: dict):
        with open(file=self.file, mode="w", encoding="utf-8") as config:
            config.write(dumps(data, indent=2))

    def key_exist(self, key: str):
        return key in self.data


def press_to_exit():
    input("\nPressez sur Enter pour fermer le programme...")
    exit()
