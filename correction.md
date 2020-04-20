## Projet de session pour le cours INF5190

### Cette documentation a pour but d'expliquer ce que contient ce projet de session.

#### A1 - Importation des données XML de la ville de Montréal
    Importation des données initiales se font manuellement. 
    On exécute simplement le projet comme un simple projet python 
    
```bash
    python3 index.py
```

#### A2 - La page d'aaueil offre une recherche dans la base de données.
    On peut y accéder via le lien suivant au niveau de la 2e section de la page web.    
   [Page de recherche](http://127.0.0.1:5000)
   
#### A3 - Une mise à jour des nouveaux contrevenants sera effectuées à chaque jour à 00:00.
    Cette tache possède une fonction dans le fichier index.py 
    qui se nommme mise_jour_contrevenants et qui sera appelée à la fin d'index.py.

#### A4 - Un service REST permettant d'avoir la liste des contrevenants pendant un interval de temps.
    Nous devons utiliser la méthode GET avec la route
    Ce service peut être utiliser via la route suivante :
        En utilisant deux paramètres obligatoires soit «du» et «au».     
    
* http://127.0.0.1:5000/api/liste_amendes_etablissement/interval?du=2015-09-30&au=2015-10-05

#### A5 - Une interface web pour utiliser le service REST fait en A4.
    Le service rest sera utilisé via un appel ajax avec la méthode Post inclu dans la route.
    On peut y accéder via le lien suivant au niveau de la 1ère section de la page web.
    On doit aussi fournir les paramètres obligatoires.
    L'information sera afficher sosu le formulaire dans la section
* Résultat 1 - Une liste des établissements avec leur nombre amendes

   [Page de recherche](http://127.0.0.1:5000)

#### A6 - On utilise la même interface web qu'en A5 mais avec une 2e option de recherche par établissement
    Cette 2e option utilisera une route différente comme on veut faire afficher 
    la liste des contravention d'un établissement
    Cette option de recherche se trouve toujours dans la 1ère section de l'interface web.
   [Page de recherche](http://127.0.0.1:5000)
* Résultat 2 - Toutes l'information sur les amendes d'un établissement sélectionnémendes
   
* http://127.0.0.1:5000/api/liste_amendes_etablissement/etablissement?choix=ALIMENTATION GUSTA

#### B1

   

   




   
    