from argparse import ArgumentParser

from classes.gui_classe import *
from classes.rpc_class import RPC

main_menu = ArgumentParser(description="PlexRPC for Discord")
main = main_menu.add_argument_group("Main arguments")
main.add_argument("-s", "--setup", help="Allow you to setup your credentials", action='store_true')
main.add_argument("-r", "--run", help="Allow you to run the scripts", action='store_true')
choice = main_menu.parse_args()

if __name__ == "__main__":
    if choice.setup:
        welcome = GUI()
        welcome.resize
        welcome.rename("Configuration Initiale")
        welcome.username(0, 0)
        welcome.password(1, 0)
        welcome.connect_button("Se connecter")
        welcome.run
    if choice.run:
        discord_rpc = RPC()
        discord_rpc.do_loop
