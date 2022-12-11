from classes.gui_classe import *
from classes.rpc_class import RPC
from sys import argv

try:
    argv[1]
except:
    print("Vous devez spécifier soit:\n --setup (Configurer le script)\n --run (executer le script)")
    exit()

if __name__ == "__main__" and argv[1] == "--setup":
    welcome = GUI()
    welcome.resize
    welcome.rename("Configuration Initiale")
    welcome.username(0, 0)
    welcome.password(1, 0)
    welcome.connect_button("Se connecter")
    welcome.run

if __name__ == "__main__" and argv[1] == "--run":
    discord_rpc = RPC()
    discord_rpc.do_loop