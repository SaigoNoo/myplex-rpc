from plexapi.server import PlexServer
from plexapi.utils import plexOAuth
from plexapi.exceptions import Unauthorized

from .usual_functions import val_key, save_value


class Plex:
    @staticmethod
    def check_connect():
        """
        Si le token de connexion n'est plus valide, un nouveau sera crée par authentification oAuth2.
        __PRE__:
        - le fichier de config.json doit exister
        - le fichier de config.json doit avoir un premier niveau de clé "plex"
        - le fichier de config.json doit avoir dans la clé "plex":
            - "token": Qui doit être un <str> soit hardcodé (pas nécessaire), soit obtenu via la méthode (par défaut)
            - "base_url": Qui doit être un <str> hardcodé
            - "X-Plex-Client-Identifier": Qui doit être de type <str> et identifiera quel est le nom de connexion du script dans
            la liste des appareils connectés de Plex
        __POST__:
        - sera réecrit SI on est dans le [raise: Unauthorized]:
            - "token": Qui doit être un <str> obtenu via la méthode

        """
        headers = {
            'X-Plex-Client-Identifier': val_key()["plex"]["X-Plex-Client-Identifier"],
        }
        try:
            PlexServer(baseurl=val_key()['plex']["base_url"], token=val_key()["plex"]["token"])

        except Unauthorized:
            instance = plexOAuth(headers=headers, timeout=120)
            save_value(key="token", value=instance.authenticationToken)


class PlexRPC:
    def __init__(self):
        self.instance = PlexServer(baseurl=val_key()['plex']["base_url"], token=val_key()["plex"]["token"])

    def sessions(self) -> list:
        """
        Retourne une liste d'objets des sessions actives
        __PRE__:
        - self.instance doit être instancié et contenir un objet
        __POST__:
        - Renvoie une liste d'objets non stockés
        """
        return self.instance.sessions()

    def data(self, index: int) -> dict:
        """
        Retourne un objets d'un des sessions actives a partir de son index
        __PRE__:
        - self.instance doit être instancié et contenir un objet
        - index doit être un <int>
        __POST__:
        - Renvoie un objet non stocké
        """
        return self.instance.sessions()[index]

    @staticmethod
    def state(session: object) -> str:
        """
        Retourne une string qui indique l'état de lecture d'une session selon son index
        __PRE__:
        - self.instance doit être instancié et contenir un objet
        - index doit être un <int>
        __POST__:
        - Renvoie un <str> non stocké
        """
        return session.players[0].state

    def is_session_empty(self) -> bool:
        """
        Retourne un <bool> qui indique si l'utilisateur lit actuellement sur Plex en vérifiant la longueur de la
        liste des sessions.
        __PRE__:
        - self.instance doit être instancié et contenir un objet
        - self.sessions doit être une liste d'objets
        __POST__:
        - Renvoie <bool> non stocké
        """
        return len(self.instance.sessions()) == 0
