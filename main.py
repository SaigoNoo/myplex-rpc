from argparse import ArgumentParser
from atexit import register
from time import sleep

from plexapi.utils import plexOAuth

from classes.checker import Checker
from classes.plex_classe import Plex
from classes.rpc_class import RPC
from classes.text import Text
from classes.updater import Updater
from classes.usual_functions import File, press_to_exit

# ----------------- #
#    PARAMETERS     #
# ----------------- #

arg = ArgumentParser(description="Aide de MyPlexRPC...")
arg.add_argument("-su", "--set-username",
                 help="Définir username Plex"
                 )
arg.add_argument("-sp", "--set-password",
                 help="Définir password Plex..."
                 )
arg.add_argument("-ss", "--set-server",
                 help="Définir servername Plex..."
                 )
arg.add_argument("-ssu", "--set-server-url",
                 help="Définir l'URL avec HTTPS du serveur"
                 )
arg.add_argument("-ba", "--blacklist-add",
                 help="Ajouter library blacklist..."
                 )
arg.add_argument("-bd", "--blacklist-delete",
                 help="Supprimer library blacklist..."
                 )
arg.add_argument("-cc", "--create-config",
                 help="Créer votre fichier de configuration... (AUTRES ARGS IGNORES)",
                 action="store_true"
                 )
arg = arg.parse_args()

# ----------------- #
#   DECLARATIONS    #
# ----------------- #

updater = Updater()
text = Text(module="MyPlexRPC Main")
checker = Checker(file="config.json")
if not checker.config_exist() and not arg.create_config:
    text.print(
        content="Le fichier de config.json n'existe pas, utilisez l'option -cc",
        type_text="error"
    )
    press_to_exit()
config = File(file="config.json")
rpc = RPC()

if arg.create_config:
    checker.recreate_config()
    text.print(
        content="Sauvagarde effectuée...",
        type_text="success"
    )
else:
    if arg.set_username:
        config.set_value(key="username", value=arg.set_username)
        text.print(
            content="La valeur de username a été modifiée !",
            type_text="success"
        )
    if arg.set_password:
        config.set_value(key="password", value=arg.set_password)
        text.print(
            content="La valeur de password a été modifiée !",
            type_text="success"
        )
    if arg.set_server:
        config.set_value(key="server_name", value=arg.set_server)
        text.print(
            content="La valeur de server_name a été modifiée !",
            type_text="success"
        )
    if arg.set_server_url:
        config.set_value(key="server_url", value=arg.set_server_url)
        text.print(
            content="La valeur de server_url a été modifiée",
            type_text="success"
        )
    if arg.blacklist_add:
        data = config.get_value(key="black_list")
        if arg.blacklist_add not in data:
            data.append(arg.blacklist_add)
            config.set_value(key="black_list", value=data)
            text.print(
                content="La valeur de blacklist a été modifiée !",
                type_text="success"
            )
        else:
            text.print(
                content=f"{arg.blacklist_add} est déjà encodée dans la blacklist",
                type_text="error"
            )
    if arg.blacklist_delete:
        data = config.get_value(key="black_list")
        try:
            data.remove(arg.blacklist_delete)
            config.set_value(key="black_list", value=data)
            text.print(
                content="La valeur de blacklist a été modifiée !",
                type_text="success"
            )
        except ValueError:
            text.print(
                content=f"{arg.blacklist_delete} n'est pas encodée dans la blacklist",
                type_text="error"
            )
# ----------------- #
#     CHECKER       #
# ----------------- #
text.print(
    content="Vérification des requis...",
    type_text="info"
)
checker.run_checks()

# Create A New Temp Token USER
headers = {
    'X-Plex-Client-Identifier': config.get_value(key="X-Plex-Client-Identifier")
}
token = plexOAuth(headers=headers, timeout=30)

plex = Plex(token=token.authenticationToken)

# ----------------- #
#     UPDATER       #
# ----------------- #
text.print(
    content="Vérification d'une éventuelle mise à jour...",
    type_text="info"
)
if updater.new_update_available():
    text.print(
        content="Une nouvelle version de MyPlexRPC est disponible sur GitHub !",
        type_text="warning"
    )
    text.print(
        content="Lancez le setup.py pour mettre à jour ! !",
        type_text="warning"
    )
    text.print(
        content="Fermez le script initial avant de mettre à jour !"
    )

# --------------- #
#      CODE       #
# --------------- #
text.print(
    content="Démarrage du code...",
    type_text="info"
)


def preview(activity: dict = None):
    content = None
    if activity is None:
        content = "Aucun épisode en lecture..."
    elif activity["type"] == "show":
        content = (f"Titre épisode: {activity['underTitle']}\n"
                   f"Episode: S{activity['seasonNumber']}E{activity['episodeNumber']}\n"
                   f"Temps: {str(int(activity['time'] // 3600)).zfill(2)}:{str(int(activity['time'] // 60 % 60)).zfill(2)}:{str(int(activity['time'] % 60)).zfill(2)}\n"
                   f"Status: {'Pause' if activity['status'] == 'paused' else 'Lecture'}")
    elif activity["type"] == "movie":
        print(activity["time"])
        content = (f"Genres: {activity['underTitle']}\n"
                   f"Temps: {str(int(activity['time'] // 3600)).zfill(2)}:{str(int(activity['time'] // 60 % 60)).zfill(2)}:{str(int(activity['time'] % 60)).zfill(2)}\n"
                   f"Status: {'Pause' if activity['status'] == 'paused' else 'Lecture'}")
    text.print(
        content=content,
        type_text="default"
    )


def detect_update():
    """
    Si l'activités active et la même que avant et que la session actuelle est encore active, ne rien faire
    mais dès que changement, prévenir afin de redéfinir la session
    :return:
    """
    while True:
        activity = plex.activity()
        if plex.is_session_empty():
            rpc.discord_rpc()
            preview(activity=None)
        else:
            preview(activity=activity)
            rpc.discord_rpc(activity=activity)
        sleep(1)


plex.update_values()
rpc.connect()


def close_socket():
    text.print(
        content="Arrêt forcé de MyPlexRPC...",
        type_text="warning"
    )
    plex.close()
    rpc.disconnect()


register(close_socket)

detect_update()
