# Projet de session pour le cours INF5190

## Un site web avancé qui offre plusieurs service REST.
    L'information stocké dans la base de données vient de données réels de la ville de Montréal.
    L'information est au sujet des amendes que les établissements reçoivent à la suite de plaintes 
    par les clients ou les inspectionts par la ville.

## On doit installer plusieurs modules relatifs à Python

### Les technologies principales seront :
  * Python 3.8
  * Flask 1.1
  * SQLite 3
  
On doit les installer avec les commandes suivantes :

```bash
sudo apt install python3.8
pip3 install flask
sudo apt-get install sqlite3
```
### Pour utiliser toutes les technologies secondaires nécessaire au bon déroulement du site web :
  * Jsonify
  * Apscheduler
  * YAML 
  * Email
  * RAML qui nécessitera aussi l'installation de NPM
  * Flask Json Schema
  * Flask Json Schema Validateur 
  * ElementPath (Les fichiers XML)
  * Response
  
### Voici les commandes pour faire les installations des modules secondaires :

```bash
pip3 install jsonify
pip3 install APScheduler
pip3 install pyyaml
```

  * Pour offrir un système d'envoi de courriel, nous avons besoin d'un package pour gérer le tout
```bash
pip3 install email-to  
```
  * Dans le cadre du travail, nous avons créer un compte GMAIL uniquement pour la gestion des courriel
    * b.mignault.uqam.qc.ca@gmail.com
    * Uqam123((SUPER)))
  * Les informations du courriel et password sont dans le fichier fonction.py comme constante  

  * Pour offrir une documentation  claire des services REST, on va utiliser RAML
    mais on doit installer NPM avant. 
    
    Voici la séquence d'installation :
```bash
curl -sL https://deb.nodesource.com/setup_10.x | sudo -E bash -
sudo apt install nodejs
curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.34.0/install.sh | bash
export NVM_DIR="$HOME/.nvm"
nvm install node
nvm install --lts
sudo apt update
sudo apt install nodejs
```    
  * Poursuivons avec les autres modules :
```bash
pip3 install flask-json-schema
pip3 install flask-jsonschema-validator
pip3 install elementpath
pip3 install responses
```

  * Il y a un dernier module utile à installer est celui pour valider 
    notre style de codage par rapport à la norme PEP 8.
```bash
pip install pycodestyle
pip install --upgrade pycodestyle
```

## License

* Travail présenté par Benoît Mignault étudiant de l'UQAM 
* Code permanent : MIGB09078205
* Travail remis le 2020-04-22