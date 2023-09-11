from time import sleep, time

from pypresence import Presence
from psutil import process_iter

from .plex_classe import PlexRPC
from .usual_functions import val_key


class RPC:
    def __init__(self):
        self.icon = None
        self.last_media = None
        self.session = None
        self.details = None
        self.state = None
        self.rpc = Presence(974790030335823952)
        self.dns = val_key("plex")["domain"]
        self.port = val_key("plex")["port"]
        self.token = val_key("plex")["token"]
        self.active = False
        self.wait = 3
        self.waiting_message = False
        self.last_state = None
        self.path = None
        self.large_image = None

    @property
    def do_loop(self):
        while True:
            while PlexRPC().no_listners or PlexRPC().there_listners and not PlexRPC().is_watching:
                if self.active:
                    self.active = False
                    self.disconnect

                if not self.waiting_message:
                    print("En attente d'activité...")
                    self.waiting_message = True

                sleep(self.wait)

            while PlexRPC().is_watching:
                if self.last_state is None:
                    self.last_state == PlexRPC().paused
                    self.last_media = PlexRPC().what_watching.ratingKey

                if not self.active:
                    self.connect
                    self.active = True
                    self.waiting_message = False

                if PlexRPC().paused != self.last_state or PlexRPC().what_watching.ratingKey != self.last_media:
                    print(PlexRPC().output)
                    self.define_rpc
                    self.last_state = PlexRPC().paused
                    self.last_media = PlexRPC().what_watching.ratingKey

                sleep(self.wait)

    @property
    def connect(self):
        print("Waiting than Discord load...")
        for process in process_iter(['name']):
            if process.info['name'] == 'Discord':
                print("Discord is now ready...")
                self.rpc.connect()
                return True
        return False

    @property
    def disconnect(self):
        self.rpc.close()

    @property
    def define_rpc(self):
        self.session = PlexRPC().what_watching
        self.path = self.session.show().locations[0]
        self.large_image = f'{self.dns}:{self.port}{self.session.thumb}?X-Plex-Token={self.token}'

        if self.session.type == "track":
            self.details = self.session.title
            self.state = self.session.artist().title

        elif self.session.type == "episode":
            self.details = self.session.show().title
            self.state = f"{self.session.title} (S{self.session.seasonNumber}E{str(self.session.episodeNumber).zfill(2)})"

        elif self.session.type == "movie":
            self.details = self.session.title
            self.state = " ".join(str(f"{e}, ") for e in self.session.genres)
            self.state = self.state[:-2]

        self.discord_rpc_pause if PlexRPC().paused else self.discord_rpc_play

    @property
    def discord_rpc_play(self):
        self.rpc.update(
            details=self.details,
            state=self.state,
            large_image=self.large_image,
            large_text=self.details,
            small_image='https://cdn.icon-icons.com/icons2/2108/PNG/512/plex_icon_130854.png',
            small_text='MyPlex',
            end=int(time() + (PlexRPC().what_watching.duration / 1000) - (PlexRPC().what_watching.viewOffset / 1000))
        )

    @property
    def discord_rpc_pause(self):
        self.rpc.update(
            details=self.details,
            state=self.state,
            large_image=self.large_image,
            large_text=self.details,
            small_image='https://cdn.icon-icons.com/icons2/2108/PNG/512/plex_icon_130854.png',
            small_text='MyPlex'
        )
