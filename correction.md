## Projet de session pour le cours INF5190

### Cette documentation a pour but d'expliquer ce que contient ce projet de session.

### Il est possible d'utiliser les services REST en dehors du site web
    Pour ce faire, il faut installer un utilitaire dans votre fureteur.
    
    Exemple pour Chrome : Yet Another REST Client 

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
    Cette fonction appellera la fonction mise_jour_bd du fichier fonction.py  

#### A4 - Un service REST permettant d'avoir la liste des contrevenants pendant un interval de temps.
    Nous devons utiliser la méthode GET avec la route
    Ce service peut être utiliser via la route suivante :
        En utilisant deux paramètres obligatoires soit «du» et «au».     
    
* http://127.0.0.1:5000/api/liste_des_contrevenants/interval?du=2015-09-30&au=2015-10-05

#### A5 - Une interface web pour utiliser le service REST fait en A4.
    Le service rest sera utilisé via un appel ajax avec la méthode Post inclu dans la route.
    On peut y accéder via le lien suivant au niveau de la 1ère section de la page web.
    On doit aussi fournir les paramètres obligatoires.
    L'information sera afficher sosu le formulaire dans la section
* Résultat 1 - Une liste des établissements avec leur nombre amendes

   [Page de recherche](http://127.0.0.1:5000)

#### A6 - On utilise la même interface web qu'en A5 mais avec une 2e option de recherche par établissement.
    Cette 2e option utilisera une route différente comme on veut faire afficher 
    la liste des contravention d'un établissement
    Cette option de recherche se trouve toujours dans la 1ère section de l'interface web.
   [Page de recherche](http://127.0.0.1:5000)
* Résultat 2 - Toutes l'information sur les amendes d'un établissement sélectionnémendes
   
* http://127.0.0.1:5000/api/liste_des_contrevenants/etablissement?choix=AL-BAGHDADI

##### Pour les deux prochaines taches, nous avons utilisé les informations suivantes :
* b.mignault.uqam.qc.ca@gmail.com
* Uqam123((SUPER)))

#### B1 - À la suite de la mise à jour de la tache A3, un courriel est envoyé à chaque personne du ficheir YAML.
    On doit saisir l'adresse courriel sous la variable adresse dans le fichier 
    adresse_destination.yaml qui se trouver à la racine du projet.
    
    adresse:
   
        - b.mignault@gmail.com
        - etc....
    
  Utilisateur recevra un courriel seulement, s'il y a de nouveau contrevenant 
  à la suite de la mise à jour de la base de donnée via la tache A3.
 
#### B2 - Pour chaque nouveau contrevenant, un tweet sera envoyé.
Dans le cadre du projet, nous avons créé un compte tweeter générique.
Les api seront :
    
* API_KEY = "nIOLstoH2fvZllC6Vo8QpcpKP"
* API_SECRET = "PoX7IFqCuKKMBjoYD4diGag3XgkWF4JthQ5ZsItt17TWtl3bIW"
* ACCESS_TOKEN = "1243952698556383232-Qv98BnYtkFj8mje95QXox6yvLSUUTl"
* ACCESS_TOKEN_SECRET = "8nclhl82lk4P52CLYTIQz94vHwlod3djHRzOcdNMq4iQ8"

#### C1 - Un service REST pour obtenir la liste des établissements et leur quantité d'infraction
    L'information est retourné en format JSON
    On a simplement à utliser le lien suivant :
    
   [Lien pour obtenir l'information](http://127.0.0.1:5000/api/liste_des_contrevenants/json) 
   
#### C2 - Un service REST pour obtenir la liste des établissements et leur quantité d'infraction
    L'information est retourné en format XML
    On a simplement à utliser le lien suivant :
    
   [Lien pour obtenir l'information](http://127.0.0.1:5000/api/liste_des_contrevenants/xml) 
   
#### C3 - Un service REST pour obtenir la liste des établissements et leur quantité d'infraction
    L'information est retourné en format CSV
    On a simplement à utliser le lien suivant :
    
   [Lien pour obtenir l'information](http://127.0.0.1:5000/api/liste_des_contrevenants/csv)  

#### D1 - Un service REST pour créer une plainte d'un établissement
    Le service REST va récolter les informations nécessaire en JSON. 
    Ces dernières doivent correspondre à la forme escompté via le fichier de 
    validation JSON écrit en python.
    
    Ce fichier se trouve dans le dossier :
    /json_schema pour le fichier validateur_plainte.py
    
    On ne peut pas simplement utiliser le lien suivant :
   [Lien pour créer une plainte](http://127.0.0.1:5000/api/nouvelle_plainte) 
   
   On doit ajouter les informations sous le format JSON
    
    {
        "etablissement": "AILE BUFFALO BILL",
        "no_civique": 4084,
        "nom_rue": "Rue Saint-Denis",
        "ville": "Montréal H2W 2M5",
        "date_visite": "2018-05-28",
        "prenom_plaignant": "Benoît",
        "nom_plaignant": "Mignault",
        "description": "Nous avons remarqué la présence de petits animaux."
    }
    
Une fois la plainte crée, le service va retourner le ID de la plainte 
qui sera utile pour la tache suivante
    
#### D2 - Un service REST pour supprimer une plainte qu'on aurait crée
    Le service REST aura besoin du id que le résultat du service REST de la tache 
    précédente nous aura communiquer.
    
    Je ne peux mettre de lien cliquable vue que nous avons besoin d'un paramètre 
    à la fin de l'URL.
    
    Voici un exemple :

* http://127.0.0.1:5000/api/plainte/34

#### E1 - Un service REST pour créer un profil utilisateur.
    Ce profil utilisateur aura pour but de gérer les établissements à surveiller.
    
    Ces dernières doivent correspondre à la forme escompté via le fichier de 
    validation JSON écrit en python.
    
    Ce fichier se trouve dans le dossier :
    /json_schema pour le fichier validateur_profil.py
    
    On ne peut pas simplement utiliser le lien suivant :
   [Lien pour créer un profil](http://127.0.0.1:5000/api/nouveau_profil) 
   
   On doit ajouter les informations sous le format JSON
    
    {
        "nom": "Mignault",
        "prenom": "Benoit",
        "password": "Patate123(((",
        "courriel": "b.mignault@gmail.com",
        "liste_etablissement": 
        [
           "PIZZA EXPRESSO", "ALIMENTS MARINA"
        ]
    }
    
Un message de succès sera produit si tout ce passe bien, sinon un message 
d'erreur sera affiché si le courriel est déjà présent dans la base de donnée

#### E2 - Cette tache comprendra plusieurs choses.
* Une interface web pour créer un profil qui sera envoyer via Ajax au service RESt de la tache E1

Cette interface web est disponible à la l'adresse suivante : 

[Lien pour créer un profil](http://127.0.0.1:5000/nouveau_profil) 

* Une fois le profil crée, l'utilisateur est invité à se diriger vers le lien web suivant :

[Lien pour se connecter à notre profil](http://127.0.0.1:5000/connection)

En utilisant son courriel et mot de passe

* Une fois connecter, l'utilisateur va pouvoir gérer sa photo de profil (format jpg et png) et sa liste des établissements à surveiller
 
#### E3 - Cette tache est la suite de la tache B1
    Elle consistera à envoyer un courriel à l'utilisateur qui aurait décidé 
    de suivre l'établissement qui vient de recevoir une contravention.
    
    Cette gestion est possible grâce à la page de gestion de ses établissements 
    à surveiller.    
    
    Le processus est automatique à chaque jour à minuit (00:00)

#### E4 - Envoi un courriel comme en E3 mais avec un lien pour se désabonner
    L'utilisateur aura 6 heures au moment de la réception du courriel pour se désabonner.
    
    Le lien mènera vers une page web :
    
    Voici un exemple :    
* http://127.0.0.1:5000//connecter/desabonnement/3fb4bf248645c4048e2166a26c0ea87ceb535b18de7112ba678db440f7686b225d9a171ecd25f0472394f9c3610b5fe327ef63f258faadc4008b9ee1ca09f487
    
    Au moment de vouloir supprimer l'abonnement, nous vérifions encore une fois 
    si le lien est valide et si le temps est encore disponible.
    
    Un service REST avec la méthode «Delete» sera invoquer pour détruire le suivi de l'abonnement.
    Via la route : /api/connecter/desabonnement