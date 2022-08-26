import json
from os import getenv
from sys import platform
from time import sleep, time

from plexapi.server import PlexServer
from pypresence import Presence

# Variables / Array
plexArray = []
waitTime = 1
win = "USERPROFILE"
linux = "user"
last_rk = ""
status = "OFF"
status = True
pause = False

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


# Functions
def update_metas(array, session_var, token_var):
    array.clear()

    if session_var.type == "track":
        array += [session_var.title]
        array += [session_var.artist().title]
        array += [f"{full_url}{session_var.thumb}?X-Plex-Token={token_var}"]
    elif session_var.type == "episode":
        array += [session_var.show().title]
        array += [f"{session_var.title} (S{session_var.seasonNumber}E{str(session_var.episodeNumber).zfill(2)})"]
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
        small_image="https://i.imgur.com/Mm7Aq0N.png",
        end=int(time() + (session_var.duration / 1000) - (session_var.viewOffset / 1000))
    )


def update_presence_pause(array):
    rpc.update(
        details=str(array[0]),
        state=str(array[1]),
        large_image=str(array[2]),
        large_text=str(array[0]),
        small_image="https://i.imgur.com/oWPsNN4.png"
    )


def isUser(allowed, detected):
    if allowed in detected:
        return True
    else:
        return False


def rpc_Connected(status):
    if status == "ON":
        return True
    else:
        return False


def plex_hasChange(rk, l_rk):
    if rk == l_rk:
        return False
    else:
        return True


# Presence Loop
rpc = Presence(data["discord_id"])

while True:
    while len(plex.sessions()) == 0:
        sleep(waitTime)
        print("In waiting of new activity !")
        if rpc_Connected(status):
            rpc.close()
            status = "OFF"

    while len(plex.sessions()) > 0:
        for [index, session] in enumerate(plex.sessions()):
            if isUser(user, session.usernames):
                if not rpc_Connected(status):
                    rpc.connect()
                    status = "ON"

                if not last_rk:
                    update_metas(plexArray, session, token)
                    last_rk = session.ratingKey
                    update_presence(plexArray, session)
                    print(f"Media detected: {plexArray[0]}")
                    sleep(waitTime)

                if plex_hasChange(session.ratingKey, last_rk):
                    update_metas(plexArray, session, token)
                    last_rk = session.ratingKey
                    update_presence(plexArray, session)
                    print(f"Media detected: {plexArray[0]}")
                    sleep(waitTime)

                if session.players[0].state == "paused":
                    if not pause:
                        print("Media paused !")
                        sleep(waitTime)
                        update_presence_pause(plexArray)
                    pause = True

                if session.players[0].state == "playing" and pause:
                    print("Media resumed !")
                    sleep(waitTime)
                    update_presence(plexArray, session)
                    pause = False