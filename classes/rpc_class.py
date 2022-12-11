from pypresence import Presence
from time import sleep, time
from .plex_classe import PlexRPC
from .usual_functions import val_key


class RPC:
    def __init__(self):
        self.rpc = Presence(974790030335823952)
        self.https = "https://" if val_key("plex")["https"] else "http://"
        self.dns = val_key("plex")["domain"]
        self.port = val_key("plex")["port"]
        self.token = val_key("plex")["token"]
        self.active = False
        self.wait = 5
        self.waiting_message = False
        self.last_state = None

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
                if self.last_state == None:
                    self.last_state == PlexRPC().paused
                    self.last_media = PlexRPC().what_watching.ratingKey

                if not self.active:
                    self.connect
                    self.active = True
                    self.waiting_message = False

                self.icon = "https://i.imgur.com/oWPsNN4.png" if PlexRPC().paused else "https://i.imgur.com/Mm7Aq0N.png"
                if PlexRPC().paused != self.last_state or PlexRPC().what_watching.ratingKey != self.last_media:
                    print(PlexRPC().output)
                    self.define_RPC
                    self.last_state = PlexRPC().paused
                    self.last_media = PlexRPC().what_watching.ratingKey

                sleep(self.wait)

    @property
    def connect(self):
        self.rpc.connect()

    @property
    def disconnect(self):
        self.rpc.close()

    @property
    def define_RPC(self):
        self.session = PlexRPC().what_watching
        if self.session.type == "track":
            self.details = self.session.title
            self.state = self.session.artist().title
            self.large_image = self.session.thumb

        elif self.session.type == "episode":
            self.details = self.session.show().title
            self.state = f"{self.session.title} (S{self.session.seasonNumber}E{str(self.session.episodeNumber).zfill(2)})"
            self.large_image = self.session.show().thumb

        elif self.session.type == "movie":
            self.details = self.session.title
            self.state = " ".join(str(f"{e}, ") for e in self.session.genres)
            self.state = self.state[:-2]
            self.large_image = self.session.thumb

        self.discord_rpc_pause if PlexRPC().paused else self.discord_rpc_play

    @property
    def discord_rpc_play(self):
        self.rpc.update(
            details=self.details,
            state=self.state,
            large_image=f'{self.https}{self.dns}:{self.port}{self.large_image}?X-Plex-Token={self.token}',
            large_text=self.details,
            small_image=self.icon,
            end=int(time() + (PlexRPC().what_watching.duration / 1000) - (PlexRPC().what_watching.viewOffset / 1000))
        )

    @property
    def discord_rpc_pause(self):
        self.rpc.update(
            details=self.details,
            state=self.state,
            large_image=f'{self.https}{self.dns}:{self.port}{self.large_image}?X-Plex-Token={self.token}',
            large_text=self.details,
            small_image=self.icon,
        )
