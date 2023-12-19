from pypresence import Presence
from pypresence.exceptions import DiscordNotFound

from .gui_classe import GUI
from .plex_classe import PlexRPC
from .usual_functions import val_key


class RPC:
    def __init__(self):
        self.rpc = Presence(974790030335823952)
        self.baseurl = val_key()["plex"]["base_url"]
        self.token = val_key()["plex"]["token"]
        self.details = None
        self.state = None
        self.connected = False

    def do_loop(self):
        main = GUI(text="MyPlexRPC")
        main.create_sessions_list(sessions=PlexRPC().sessions(), event_method=self.run_rpc)
        main.run()
        self.disconnect()

    def run_rpc(self, event):
        if not self.connected:
            self.connect()
            self.connected = True
        index = event.widget.curselection()[0]
        self.define_rpc(session=PlexRPC().data(index=index))

    def connect(self):
        try:
            self.rpc.connect()
            return True
        except DiscordNotFound:
            return False

    def disconnect(self):
        try:
            self.rpc.close()
            self.connected = False
            return True
        except ConnectionError:
            return False

    def define_rpc(self, session: object):
        self.path = session.show().locations[0]
        self.large_image = f'{self.baseurl}{session.thumb}?X-Plex-Token={self.token}'

        if session.type == "episode":
            self.details = session.show().title
            self.state = f"{session.title} (S{session.seasonNumber}E{str(session.episodeNumber).zfill(2)})"
        elif session.type == "movie":
            self.details = session.title
            self.state = " ".join(str(f"{e}, ") for e in session.genres)
            self.state = self.state[:-2]
        self.discord_rpc()

    def discord_rpc(self):
        self.rpc.update(
            details=self.details,
            state=self.state,
            large_image=self.large_image,
            large_text=self.details,
            small_image='https://cdn.icon-icons.com/icons2/2108/PNG/512/plex_icon_130854.png',
            small_text='MyPlex'
        )
