from json import load

from requests import get


class Updater:
    def __init__(self):
        self.data = self.read_file()

    @staticmethod
    def read_file():
        with open(file="current.json", mode="r", encoding="utf-8") as file:
            return load(file)

    def current_version(self):
        return self.data["version_date"]

    @staticmethod
    def last_commit():
        commits = get("https://api.github.com/repos/SaigoNoo/myplex-rpc/commits")
        return commits.json()[0]

    def new_update_available(self):
        return self.current_version() != self.last_commit()["commit"]["committer"]["date"]
