import time
from tkinter import *
from .plex_classe import Plex
from .usual_functions import val_key, save_value


class GUI:
    def __init__(self):
        self.pad = val_key("paddings")
        self.window = Tk()

    def resize(self, x, y):
        self.window.geometry(f"{x}x{y}")

    def rename(self, sentence):
        self.window.title(f"{sentence}")

    def login(self, x, y):
        Label(self.window, text="Nom d'utilisateur: ").grid(row=x, column=y)
        Label(self.window, text="Mot de passe: ").grid(row=x + 1, column=y)

        self.user = Entry(self.window)
        self.passwd = Entry(self.window, show='●')

        self.user.insert(0, val_key("plex")["username"])
        self.passwd.insert(0, val_key('plex')["password"])

        self.user.grid(row=x, column=y + 1)
        self.passwd.grid(row=x + 1, column=y + 1)

        Button(self.window,
               text=f"Se connecter à Plex",
               fg='#cc7b19',
               command=lambda: self.get_token,
               padx=self.pad["x"],
               pady=self.pad["y"],
               background='#1e1e1e').place(relx=0.5, rely=0.5, anchor=CENTER)

    @property
    def get_token(self):
        try:
            self.plex_access = Plex(self.user.get(), self.passwd.get()).get_token
            save_value("token", self.plex_access.authenticationToken)
            save_value("username", self.user.get())
            save_value("password", self.passwd.get())
            self.window.destroy()
        except:
            error_login = self.GUI()

    @property
    def run(self):
        return self.window.mainloop()
