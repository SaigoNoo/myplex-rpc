from os import getenv, system, rename, mkdir
from os.path import exists
from sys import platform
import requests
from subprocess import call

win = "USERPROFILE"
linux = "user"

# Req
system("pip3 install -r requirments.txt")

# Config Load
if platform == "win32":
    path = f"{getenv(win)}\.myplex-rpc\config.json"
    executable = "Notepad.exe"
    bootdir = f"{getenv(win)}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\myplex-rpc.pyw"
elif platform == "linux":
    path = f"{getenv(linux)}/.myplex-rpc/config.json"
    executable = "gedit"  # Au choix, nano, micro, gedit, ...
    bootdir = "/bin/myplex-rpc.pyw"

if not exists(path):
    try:
        rename("config.json", path)
    except:
        if not exists(path.replace("config.json", "")):
            mkdir(path.replace("config.json", ""))

        if not exists("config.json"):
            response = requests.get("https://raw.githubusercontent.com/SaigoNoo/myplex-rpc/main/config.json")
            open("config.json", "wb").write(response.content)

        rename("config.json", path)

if not exists(bootdir):
    try:
        rename("run.pyw", bootdir)
    except:
        if not exists("run.pyw"):
            response = requests.get("https://raw.githubusercontent.com/SaigoNoo/myplex-rpc/main/run.pyw")
            open("run.pyw", "wb").write(response.content)

        rename("run.pyw", bootdir)


if input("Avez-vous déjà édité le fichier de config (y/n):") == "n":
    system(f"{executable} {path}")

print("Voilà ! Le tout est prêt ! Observez l'activité sur votre profil et forcez l'arret de cette fenêtre !")
call(f"{bootdir}", shell=True)
