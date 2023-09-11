from plexapi.myplex import MyPlexAccount
from plexapi.server import PlexServer

from .usual_functions import val_key


class Plex:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    @property
    def get_token(self):
        return MyPlexAccount(username=self.username, password=self.password)


class PlexRPC:
    def __init__(self):
        self.plex = val_key("plex")
        self.instance = PlexServer(
            f'{self.plex["domain"]}:{self.plex["port"]}',
            self.plex["token"])
        self.username = val_key("plex")["username"]

    @property
    def what_watching(self):
        for session in self.instance.sessions():
            if self.username in session.usernames:
                return session

    @property
    def is_watching(self):
        for session in self.instance.sessions():
            if self.username in session.usernames:
                return True
        return False

    @property
    def no_listners(self):
        return True if len(self.instance.sessions()) == 0 else False

    @property
    def there_listners(self):
        return True if len(self.instance.sessions()) > 0 else False

    @property
    def paused(self):
        return True if self.what_watching.players[0].state == "paused" else False

    @property
    def output(self):
        return f"{self.what_watching.title} | State: {'paused' if self.paused else 'playing'}"
