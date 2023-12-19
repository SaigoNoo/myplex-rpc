from tkinter import Tk, Label, Button, Listbox, LEFT, TOP, RIGHT, END
from .plex_classe import PlexRPC


class GUI:
    def __init__(self, text: str):
        self.account = None
        self.plex_access = None
        self.size = {"x": 450, "y": 150}
        self.pad = {"x": 20, "y": 5}
        self.window = None
        self.text = text
        self.create_window()
        self.selected_value = None

    def create_window(self) -> None:
        """
        Crée une interface GUI avec le strict minimum !
        __PRE__:
        - self.text ne doit pas être <None>, sinon le titre de page sera erroné
        - self.size doit être un <dict>, et contenir:
            - une entée X de type <int>
            - une entrée Y de type <int>
        __POST__:
        - l'attribut <obj>.newGeometry sera modifié
        - l'attribut <obj>.string sera réecrit
        """
        self.window = Tk()
        self.window.geometry(f"{self.size['x']}x{self.size['y']}")
        self.window.title(f"{self.text}")

    def create_sessions_list(self, sessions: list, event_method):
        """
        Permet à Tkinter d'ajouter une liste cliquable d'éléments.
        __PRE__:
        - sessions doit être une <list> de <objet>
        - event_method doit être une <classmethod>
        __POST__:
        - self.window sera alteré par ses nouveaux attributs:
            - taille de la fenetre
            - liste
            - boutons
            - labels
        :return:
        """
        Label(self.window, text="Liste de vos sessions actives").pack(side=TOP)
        listbox = Listbox(self.window, width=40, height=10)
        listbox.pack(side=RIGHT)
        Button(
            self.window,
            text="Actualiser la liste",
            command=lambda: self.reset_listbox(listbox_object=listbox, sessions=PlexRPC().sessions())
        ).pack(side=LEFT, padx=50, pady=0)
        if not PlexRPC().is_session_empty():
            for session in sessions:
                listbox.insert(END, f"{session.show().title}: {session.title}")
        listbox.bind("<<ListboxSelect>>", event_method)

    @staticmethod
    def reset_listbox(listbox_object: object, sessions: list):
        """
        Permet de réeinitialiser la liste des sessions sur Tkinter
        __PRE__:
        - une listebox <classmethod> venant de Tkinter existant
        - sessions: <list> de <object>
        __POST__:
        - Réecriture des attributs de la listebox de tkinter
        """
        listbox_object.delete(0, END)
        if not PlexRPC().is_session_empty():
            for session in sessions:
                listbox_object.insert(END, f"{session.show().title}: {session.title}")

    def run(self):
        return self.window.mainloop()
