from tkinter import *
from .plex_classe import Plex
from .usual_functions import val_key, save_value


class GUI:
    def __init__(self):
        self.size = val_key("window")
        self.pad = val_key("paddings")
        self.window = Tk()

    @property
    def resize(self):
        self.window.geometry(f"{self.size['x']}x{self.size['y']}")
        return 0

    def rename(self, sentence):
        self.window.title(f"{sentence}")

    def connect_button(self, sentence):
        Button(self.window,
               text=f"{sentence}",
               command=lambda: self.get_token,
               padx=self.pad["x"],
               pady=self.pad["y"]).place(relx=0.5, rely=0.5, anchor=CENTER)

    def username(self, x, y):
        Label(self.window, text="Nom d'utilisateur: ").grid(row=x, column=y)
        self.user = Entry(self.window)
        self.user.insert(0, val_key("plex")["username"])
        self.user.grid(row=x, column=y + 1)

    def password(self, x, y):
        Label(self.window, text="Mot de passe: ").grid(row=x, column=y)
        self.passwd = Entry(self.window, show="*")
        self.passwd.insert(0, val_key("plex")["password"])
        self.passwd.grid(row=x, column=y + 1)

    @property
    def get_token(self):
        try:
            self.plex_access = Plex(self.user.get(), self.passwd.get()).get_token
            save_value("token", self.plex_access.authenticationToken)
            save_value("username", self.user.get())
            save_value("password", self.passwd.get())
            self.window.destroy()
        except:
            raise Exception("Bad Login")

    @property
    def run(self):
        return self.window.mainloop()
