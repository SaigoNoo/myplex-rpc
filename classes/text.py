from os import system as command
from platform import system
from time import sleep

from rich.console import Console
from rich.panel import Panel


class Text:
    def __init__(self, module: str, width: int = None, height: int = None, padding: int = 1):
        self.module = module
        self.size = {
            "w": width,
            "h": height
        }
        self.padding = padding

    @staticmethod
    def clear_screen():
        """
        Petite fonction simple qui clear le screen afin de faire un semblant de raffraichissement d'écran
        cls pour Windows et clear pour Unix
        :return: exec
        """
        if system() == "Linux":
            command('clear')
        elif system() == "Windows":
            command('cls')

    def print(self, content: str, type_text: str = "default"):
        """
        Réecriture de la fonction print
        :param content:
        :param type_text:
        :return:
        """
        sleep(1)
        color = None
        if type_text == "error":
            color = "red"
        elif type_text == "info":
            color = "blue"
        elif type_text == "success":
            color = "green"
        elif type_text == "warning":
            color = "yellow"
        elif type_text == "default":
            color = "white"

        self.clear_screen()
        Console(record=True).print(
            Panel.fit(
                content,
                title=self.module,
                subtitle="MyPlexRPC",
                title_align="left",
                subtitle_align="right",
                border_style=color,
                width=self.size["w"],
                height=self.size["h"],
                padding=self.padding
            )
        )

    def input(self, content: str, output: str = "str"):
        self.print(content, type_text="info")
        response = input("> ")
        if output == "str":
            return response
        elif output == "list":
            temp = []
            for item in response.split(","):
                temp.append(item.strip())
            return temp
