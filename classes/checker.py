from os.path import exists

from classes.text import Text
from classes.usual_functions import press_to_exit, File

text = Text(module="MyPlexRPC Checker")


class Checker(File):
    @staticmethod
    def config_exist():
        return exists(path="config.json")

    def recreate_config(self):
        username = text.input(
            content="Veuillez définir un username"
        )
        password = text.input(
            content="Veuillez définir un password"
        )
        server_name = text.input(
            content="Veuillez définir un serverName"
        )
        server_url = text.input(
            content="Veuillez définir un serverUrl"
        )
        blacklist = text.input(
            content="Nom des bibliothèques à bloquer",
            output="list"
        )
        result = {
            "server_name": server_name,
            "username": username,
            "password": password,
            "X-Plex-Client-Identifier": "MyPlexRPC",
            "black_list": blacklist,
            "server_url": server_url
        }
        self.write_to_file(data=result)

    def run_checks(self):
        if not self.have_username():
            text.print(
                content="> Username: Aucune valeur [Utilisez -h]",
                type_text="error"
            )
            press_to_exit()
        if not self.have_password():
            text.print(
                content="> Password: Aucune valeur [Utilisez -h]",
                type_text="error"
            )
            press_to_exit()
        if not self.have_servername():
            text.print(
                content="> ServerName: Aucune valeur [Utilisez -h]",
                type_text="error"
            )
            press_to_exit()
        if not self.have_server_url():
            text.print(
                content="> ServerURL: Aucune valeur [Utilisez -h]",
                type_text="error"
            )
            press_to_exit()

    @staticmethod
    def is_valid(value):
        return value.strip() != ""

    def have_server_url(self):
        val = self.get_value(key="server_url")
        if not val:
            text.print(
                content="> ServerURL n'existe pas [Utilisez -h]",
                type_text="error"
            )
            press_to_exit()
        else:
            return self.is_valid(value=val)

    def have_username(self):
        val = self.get_value(key="username")
        if not val:
            text.print(
                content="> Username n'existe pas [Utilisez -h]",
                type_text="error"
            )
            press_to_exit()
        else:
            return self.is_valid(value=val)

    def have_password(self):
        val = self.get_value(key="password")
        if not val:
            text.print(
                content="> Password n'existe pas [Utilisez -h]",
                type_text="error"
            )
            press_to_exit()
        else:
            return self.is_valid(value=val)

    def have_servername(self):
        val = self.get_value(key="server_name")
        if not val:
            text.print(
                content="> ServerName n'existe pas [Utilisez -h]",
                type_text="error"
            )
            press_to_exit()
        else:
            return self.is_valid(value=val)
