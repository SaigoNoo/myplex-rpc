from pypresence import Presence
from time import time


class RPC:
    def __init__(self):
        self.rpc = Presence(974790030335823952)
        self.connected = False

    def connect(self):
        if self.connected:
            return "RPC_ALREADY_ENABLE"
        else:
            self.rpc.connect()

    def disconnect(self):
        if self.connected:
            self.connected = False
            self.rpc.close()
        else:
            return "RPC_ALREADY_DISABLE"

    def discord_rpc(self, activity: dict or None = None):
        state = None
        title = None
        pic = None
        if activity is not None and activity["type"] == "movie":
            state = activity["underTitle"]
            title = f"{activity['mainTitle']} | {activity['underTitle']}"
            pic = activity["cover"]
        elif activity is not None:
            state = f"{activity['underTitle']} | S{activity['seasonNumber']}E{activity['episodeNumber']}"
            title = f"{activity['mainTitle']} | {activity['underTitle']}"
            pic = activity["cover"]
        elif activity is None:
            title = "Page d'accueil"
            state = "Recherche quelque chose à regarder..."
            pic = "https://i.imgur.com/TLOfKRp.png"
        self.rpc.update(
            details=title,
            state=state,
            large_image=pic,
            large_text=activity["mainTitle"] if activity is not None else "Accueuil Plex",
            small_image='https://play-lh.googleusercontent.com/slZYN_wnlAZ4BmyTZZakwfwAGm8JE5btL7u7AifhqCtUuxhtVVxQ1mcgpGOYC7MsAaU',
            small_text='MyPlex',
            end=None if activity is None else max(1, time() + (activity['time'] - activity['progress']))
        )
