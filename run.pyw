import json
import time
from plexapi.server import PlexServer
from pypresence import Presence
from os import system, getenv
from sys import platform

# Variables / Array
plexArray = []
waitTime = 1
connect = False
change = False
last = ""
start = True
win = "USERPROFILE"
linux="user"

# Config Load
if platform == "win32":
    path = f"{getenv(win)}\.myplex-rpc\config.json"
elif platform == "linux":
    path = f"{getenv(linux)}/.myplex-rpc/config.json"

with open(path) as config:
    data = json.load(config)

    https = data["plex"]["https"]
    url = data["plex"]["url"]
    port = data["plex"]["port"]
    token = data["plex"]["token"]
    user = data["plex"]["user"]

full_url = f"{'https' if https else 'http'}://{url}:{port}"
plex = PlexServer(full_url, token)

# Wait a activity to start !
while len(plex.sessions()) == 0:
    print(f"En l'attente d'une activité du coté serveur... {waitTime} secondes...")
    time.sleep(waitTime)


# Functions
def update_metas(array, session_var, token_var):
    array.clear()

    if session_var.type == "track":
        array += [session_var.title]
        array += [session_var.artist().title]
        array += [f"{full_url}{session_var.thumb}?X-Plex-Token={token_var}"]
    elif session_var.type == "episode":
        array += [session_var.show().title]
        array += [session_var.title]
        array += [f"{full_url}{session_var.show().thumb}?X-Plex-Token={token_var}"]
    elif session_var.type == "movie":
        array += [session_var.title]
        genres = ""
        for genre in session_var.genres:
            genres += f"{str(genre).split(':')[2].replace('>', '')} "
        array += [genres.replace(" ", ", ")[:-1]]
        array += [f"{full_url}{session_var.thumb}?X-Plex-Token={token_var}"]
        array += [session_var.duration]


def update_presence(array, session_var):
    rpc.update(
        details=str(array[0]),
        state=str(array[1]),
        large_image=str(array[2]),
        large_text=str(array[0]),
        end=int(time.time() + (session_var.duration / 1000) - (session_var.viewOffset / 1000))
    )


def as_change(last_var, actual):
    if str(last_var) != str(actual.ratingKey):
        return True
    else:
        return False


# Presence Loop
rpc = Presence(data["discord_id"])

while True:
    if len(plex.sessions()) == 0:
        connect = False
        rpc.close()

    while len(plex.sessions()) == 0:
        time.sleep(waitTime)
        print("En attente d'activité !")

    for [index, session] in enumerate(plex.sessions()):
        if user in session.usernames:
            time.sleep(waitTime)
            if start:
                start = False
                last = str(session.ratingKey)

            print(plexArray)
            update_metas(plexArray, session, token)

            if not connect:
                connect = True
                rpc.connect()
                update_presence(plexArray, session)

            if session.players[0].state == "paused":
                update_presence(plexArray, session)

            while len(plex.sessions()) == 0:
                time.sleep(waitTime)
                print("En attente d'activité !")

            if as_change(last, session):
                last = session.ratingKey
                update_metas(plexArray, session, token)
                update_presence(plexArray, session)
