from argparse import ArgumentParser
from atexit import register

from classes.rpc_class import RPC
from time import sleep
from classes.plex_classe import Plex, PlexRPC

register(RPC().disconnect)

main_menu = ArgumentParser(description="PlexRPC for Discord")
main = main_menu.add_argument_group("Main arguments")
main.add_argument("-r", "--run", help="Allow you to run the scripts", action='store_true')
choice = main_menu.parse_args()

if __name__ == "__main__":
    if choice.run:
        while not RPC().connect():
            print("Discord n'est pas encore disponible...")
            sleep(2)
        Plex().check_connect()
        RPC().do_loop()
