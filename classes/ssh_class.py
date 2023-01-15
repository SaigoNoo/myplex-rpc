from paramiko import SSHClient, AutoAddPolicy

from .usual_functions import val_key


class SSH:
    """
    La classe SSH permet d'instancier une connexion SSH, de s'y connecter
    et d'y exécuter des commandes !
    """

    def __init__(self):
        self.domain = val_key("ssh")["domain"]
        self.port = val_key("ssh")["port"]
        self.username = val_key("ssh")["username"]
        self.password = val_key("ssh")["password"]
        self.picture_dir = val_key("plex")["temp_pictures_dir"]
        self.sftp = None
        self.instance = SSHClient()

    @property
    def connect_to_ssh(self):
        """
        connect_to_ssh permet de créer une socket entre le client et le serveur !
        La connexion restera active tant que l'instance sera existante !
        """
        return self.instance.connect(self.domain, self.port, self.username, self.password)

    @property
    def add_key(self):
        """
        add_key permet de créer une clé SSH nécessaire au fonctionnement du protocol.
        La clé s'ajoute dans le known_hosts !
        """
        return self.instance.set_missing_host_key_policy(AutoAddPolicy())

    @property
    def close(self):
        """
        close ferme la connexion SSH
        :return:
        """
        return self.instance.close()

    def content_ssh(self, directory):
        """
        content_ssh retourne le contenu du dossier variable dir
        :return:
        """
        return self.instance.exec_command(command=f"ls '{directory}'")[1].read().decode('utf-8').split('\n')

    def load_picture(self, directory, name):
        """
        content_ssh retourne le contenu du dossier variable dir
        :return:
        """
        return self.instance.exec_command(command=f"cp '{directory}/icon.png' '{self.picture_dir}{name}.png'")

    @property
    def trash_folder(self):
        return self.instance.exec_command(command=f"rm '{self.picture_dir}'*")
