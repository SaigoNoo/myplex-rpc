from os import remove, listdir
from shutil import move, rmtree
from zipfile import ZipFile

from classes.text import Text
from classes.updater import Updater
from requests import get

updater = Updater()
text = Text(module="Updater")


def delete_all():
    rmtree("classes")
    remove("main.py")
    remove("requirements.txt")
    # rmtree("new_version")


def download():
    dl = get(
        url="https://github.com/SaigoNoo/myplex-rpc/archive/refs/heads/main.zip",
        stream=True
    )
    if dl.status_code == 200:
        text.print(
            content="Téléchargement de la dernière version...",
            type_text="info"
        )
        with open('main.zip', "wb") as file:
            for chunk in dl.iter_content(chunk_size=1024):
                file.write(chunk)
            text.print(
                content="Téléchargement réussi...",
                type_text="success"
            )
    else:
        text.print(
            content="Echec du téléchargement de la dernière version...",
            type_text="error"
        )


def unzip(file: str):
    text.print(
        content="Dézzipage en cours...",
        type_text="info"
    )
    with ZipFile(file, 'r') as zip_ref:
        zip_ref.extractall()
    text.print(
        content="Dézzipage terminé...",
        type_text="success"
    )

    remove(file)

    move(
        src="myplex-rpc-main",
        dst="new_version"
    )


def deploy():
    remove("new_version/config.json")
    remove("new_version/current.json")
    remove("new_version/updater.py")
    for item in listdir("new_version"):
        move(src=f"new_version/{item}", dst="/")


if not updater.new_update_available():
    download()
    unzip(file="main.zip")
    deploy()
    delete_all()
    text.print(
        content="La mise à jour est terminée !\nVous pouvez lancer MyPlexRPC !",
        type_text="success"
    )
