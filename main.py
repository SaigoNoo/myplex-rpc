from classes.gui_classe import *
from classes.rpc_class import RPC
from argparse import ArgumentParser

arg_inst = ArgumentParser(description="Menu d'aide de MyPlexRPC")
arg_inst.add_argument("-s", "--setup", action='store_true', help="Lancer le setup mode")
arg_inst.add_argument("-r", "--run", action='store_true', help="Lancer le normal mode")
args = arg_inst.parse_args()

if __name__ == "__main__" and args.setup:
    welcome = GUI()
    welcome.resize(240, 280)
    welcome.rename("Configuration Initiale")
    welcome.login(0, 1)
    welcome.run

if __name__ == "__main__" and args.run:
    discord_rpc = RPC()
    discord_rpc.do_loop
