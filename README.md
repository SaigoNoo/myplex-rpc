# MyPlex-RPC
MyPlex-RPC est un petit programme en python utilisant pypresence et plexAPI ! Il permet de partager sa progression Plex via l'activité Discord !

## Configuration
La configuration de MyPlex-RPC se passe directement dans le fichier config.json:
```json
{
  "plex": {
    "https": true,
    "url": "myplex.domaine.be",
    "port": 443,
    "token": "yourPlexToken",
    "user": "SaigoNoo"
  },
  "discord_id": 974790030335823952
}
```
Vous pouvez obtenir votre Token en ouvrant le fichier XML dans les infos de votre média (vous devez être admin du serveur Plex), puis en copiant collant le token à la fin de l'URL !

## Installation:
L'installation est relativement simple !
```
python3 install.py
```

### ATTENTION:
Windows uniquement: Vous pouvez double cliquer sur le install-win.cmd sans ouvrir manuellement le terminal et sans specifier le chemin !

## Accèder au fichier config après installation:
### Windows:
Vous pouvez y accéder par l'outil **Éxécuter...** (WINDOWS + R)
```
%USERPROFILE%\.myplex-rpc
```

### Linux:
Il se trouve dans ce répértoire
```
/home/$USER/.myplex-rpc/
```

### MacOS:
A REMPLIR...

## Des questions ?
Je tenterai de vous y répondre dans la mesure du possible !
Je suis plus facilement accessible sur Discord: SaigoNoo#3044
