# Metro_Paris

# But Du Projet : 

Le but du projet est de réaliser une application pour visualiser le trajet de métro le plus rapide pour rejoindre 2 points d’une ville (Paris).

# Partie 1 :

J'ai Récupéré depuis Internet des données représentant le réseau de métro d’une grande capitale ( Paris ), On aura besoin des stations (associées à leurs coordonnées GPS) et les lignes les reliant.
J'ai nettoyé les données (supprimer celles qui sont inutiles au projet), les ai mis en forme, et les ai stocké dans un jeu de fichiers sur disque, afin de pouvoir les utiliser dans la suite du projet.

# Partie 2 :

Le but est de réaliser une boite à outils (sous forme d’une bibliothèque de classes) sur laquelle s’appuiera la future application.

La bibliothèque de classes permet de :

     * charger un réseau de métro en mémoire

     * représenter graphiquement ce réseau

     * trouver le meilleur chemin pour rejoindre 2 points définis par leurs coordonnées GPS

     * visualiser ce chemin dans le graphe complet.

Le meilleur chemin est défini comme étant le plus rapide pour joindre 2 points de la ville. Il se compose :

    d’une première marche à pied, du point de départ à la première station de métro,

    d’un trajet en métro, avec ou sans correspondances, mais sans sortie extérieure,

    d’une seconde marche à pied, à la sortie du métro pour rejoindre le point de destination.

Les divers paramètres ( vitesse d’un marcheur, temps de trajet entre 2 stations, temps nécessaire à une correspondance, etc.) sont définis dans un fichier de configuration à part.

# Partie 3 :

Utiliser la bibliothèque précédente pour réaliser l’application qui, à partir de 2 points (définis par leurs coordonnées GPS), fournis en argument sur la ligne de commande, visualise le meilleur chemin les reliant.

