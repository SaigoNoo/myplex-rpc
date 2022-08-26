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

**A moins que vous souhaitiez un nom personalisé pour le nom de l'activité, ne changez pas le discord_id !**

![image](https://user-images.githubusercontent.com/40198990/186991403-1741aa55-f8f5-4b97-91a1-e009b262214c.png)


# Automatiser le lancement du script !

**Le fichier XML à importer se trouve dans la zone de code !**

## Windows:
<a href="http://www.youtube.com/watch?feature=player_embedded&v=sNQGLZnBhys" target="_blank"><img src="http://img.youtube.com/vi/sNQGLZnBhys/0.jpg" 
alt="IMAGE ALT TEXT HERE" width="220" height="180" border="0" /></a>

## Des questions ?
Je tenterai de vous y répondre dans la mesure du possible !
Je suis plus facilement accessible sur Discord: SaigoNoo#3044 mais vous pouvez également me faire part d'éventuelles erreurs ou sugestsions [ici](https://github.com/SaigoNoo/myplex-rpc/issues)
