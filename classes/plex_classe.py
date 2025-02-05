from plexapi.myplex import MyPlexAccount

from classes.text import Text
from classes.usual_functions import File

text = Text(module="Plex Module")


class Plex:
    def __init__(self, token: str):
        self.instance = None
        self.server_instance = None
        self.server_url = None
        self._username = None
        self.__password = None
        self.name = None
        self.token = token
        self.header_name = None
        self.current_session_id = None
        self.config = File(file="config.json")
        self.last_activity = None
        self.blacklist = []

    def close(self):
        self.instance.signout()

    def update_values(self):
        self._username = self.config.get_value(key="username")
        self.__password = self.config.get_value(key="password")
        self.name = self.config.get_value(key="server_name")
        self.header_name = self.config.get_value(key="X-Plex-Client-Identifier")
        self.instance = self.create_instance()
        self.server_instance = self.instance.resource(name=self.name).connect()
        self.server_url = self.config.get_value(key="server_url")
        self.blacklist = self.config.get_value(key="black_list")

    def create_instance(self):
        return MyPlexAccount(username=self._username, password=self.__password, token=self.token)

    def activity(self):
        for activity in self.server_instance.sessions():
            self.last_activity = activity
            if activity.user.username == self._username and activity.title not in self.blacklist:
                if activity.type == "movie":
                    return {
                        "mainTitle": activity.title,
                        "underTitle": " ".join(str(f"{e}, ") for e in activity.genres)[:-2],
                        "cover": self.replace_cover_url(target=activity.thumbUrl),
                        "progress": int(activity.viewOffset / 1000),
                        "time": int(activity.duration / 1000),
                        "type": "movie",
                        "status": activity.player.state
                    }
                elif activity.type == "episode":
                    return {
                        "mainTitle": activity.show().title,
                        "underTitle": activity.title,
                        "seasonNumber": str(activity.seasonNumber).zfill(2),
                        "episodeNumber": str(activity.episodeNumber).zfill(2),
                        "episodeCover": self.replace_cover_url(target=activity.thumbUrl),
                        "cover": self.replace_cover_url(target=activity.show().thumbUrl),
                        "progress": int(activity.viewOffset / 1000),
                        "time": int(activity.duration / 1000),
                        "type": "show",
                        "status": activity.player.state
                    }

    def current_session(self):
        for activity in self.server_instance.sessions():
            if activity.user.username == self._username:
                return activity

    def is_session_empty(self) -> bool:
        return self.activity() is None or len(self.activity()) == 0

    def replace_cover_url(self, target: str):
        return f'{self.server_url}{target.split(":32400")[1]}'
