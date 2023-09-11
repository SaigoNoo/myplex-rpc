from tkinter import *
from .plex_classe import Plex
from .usual_functions import val_key, save_value


class GUI:
    def __init__(self, text):
        self.size = val_key("window")
        self.pad = val_key("paddings")
        self.window = Tk()
        self.window.geometry(f"{self.size['x']}x{self.size['y']}")
        self.window.title(f"{text}")
        self.toggle = {
            "password_view": True
        }

    def get_token_button(self):
        Button(self.window,
               text=f"Connexion",
               command=lambda: self.get_token,
               padx=self.pad["x"],
               pady=self.pad["y"]).place(relx=0.5, rely=0.5, anchor=CENTER)

    def username(self, x, y):
        Label(
            self.window,
            text="Nom d'utilisateur: "
        ).grid(
            row=x,
            column=y
        )

        self.user = Entry(self.window)

        self.user.insert(
            0,
            val_key("plex")["username"]
        )

        self.user.grid(
            row=x,
            column=y + 1
        )

    def password(self, x, y):
        Label(self.window, text="Mot de passe: ").grid(row=x, column=y)
        self.passwd = Entry(
            self.window,
            show="•"
        )

        self.passwd.insert(
            0,
            val_key("plex")["password"]
        )

        Button(
            self.window,
            text=f"👁",
            command=lambda: self.password_view(
                self.toggle['password_view']
            )).grid(row=x, column=y + 2)

        self.passwd.grid(
            row=x,
            column=y + 1
        )

    def password_view(self, toggle):
        if toggle:
            self.passwd.configure(show='')
        else:
            self.passwd.configure(show="•")
        self.toggle['password_view'] = not toggle

    def set_domain(self, x, y):
        Label(
            self.window,
            text="Nom de domaine: "
        ).grid(
            row=x,
            column=y
        )

        Label(
            self.window,
            text="Port: "
        ).grid(
            row=x + 1,
            column=y
        )

        self.domain = Entry(self.window)
        self.port = Entry(self.window)

        self.domain.insert(
            0,
            val_key("plex")["domain"]
        )

        self.port.insert(
            0,
            val_key("plex")["port"]
        )

        self.domain.grid(
            row=x,
            column=y + 1
        )

        self.port.grid(
            row=x + 1,
            column=y + 1
        )

        Button(self.window,
               text=f"Valider",
               command=lambda: self.save_plex,
               padx=self.pad["x"],
               pady=self.pad["y"]).place(relx=0.5, rely=0.5, anchor=CENTER)

    @property
    def get_token(self):
        try:
            self.plex_access = Plex(
                self.user.get(),
                self.passwd.get()
            ).get_token

            save_value(
                "token",
                self.plex_access.authenticationToken
            )

            save_value(
                "username",
                self.user.get()
            )

            save_value(
                "password",
                self.passwd.get()
            )

            self.window.destroy()
        except:
            raise Exception("Bad Login")

    @property
    def save_plex(self):
        save_value(
            "domain",
            self.domain.get()
        )

        save_value(
            "port",
            self.port.get()
        )

        self.window.destroy()

    @property
    def run(self):
        return self.window.mainloop()
