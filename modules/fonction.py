import csv
import re  # pour la gestion des patterns pour les différents champs input
import smtplib
import xml.etree.ElementTree as ET
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from io import BytesIO, StringIO
from datetime import datetime

import hashlib
import uuid

import requests
import tweepy
from flask import g

import yaml

from .database import Database  # Importer le fichier database.py

# Lien qui sera utilisé pour récupérer les informations
URL = 'http://donnees.ville.montreal.qc.ca/dataset/a5c1f0b9-261f-4247-99d8-' \
      'f28da5000688/resource/92719d9b-8bf2-4dfd-b8e0-1021ffcaee2f/download/' \
      'inspection-aliments-contrevenants.xml'

PATTERN_PROPRIO = "^[a-z1-9A-Z][a-z0-9- 'A-Z@_!#$%^&*()<>?/\\|}{~:]{3,63}" \
                  "[a-z0-9A-Z.)]$"
PATTERN_NOM_RESTO = "^[a-z1-9A-Z][a-z0-9- 'A-Z@_!#$%^&*()<>?/\\|}{~:]{3,98}" \
                    "[a-z0-9A-Z.)]$"
PATTERN_NOM_RUE = "^[a-z1-9A-Z][a-z0-9- 'A-Z]{1,33}[a-z0-9A-Z]$"

PATTERN_DATE = "^([0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])$"

PATTERN_COURRIEL = "^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"

PATTERN_PASSWORD = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[@$!%*()?&])[A-Za-z" \
                   "\\d@()$!%*?&]{8,20}$"

SOURCE_ADRESSE = "b.mignault.uqam.qc.ca@gmail.com"

MOT_DE_PASSE = "Uqam123((SUPER)))"

# Ces API seront pour la tache B2
API_KEY = "nIOLstoH2fvZllC6Vo8QpcpKP"
API_SECRET = "PoX7IFqCuKKMBjoYD4diGag3XgkWF4JthQ5ZsItt17TWtl3bIW"
# Ces Access seront pour la tache B2
ACCESS_TOKEN = "1243952698556383232-Qv98BnYtkFj8mje95QXox6yvLSUUTl"
ACCESS_TOKEN_SECRET = "8nclhl82lk4P52CLYTIQz94vHwlod3djHRzOcdNMq4iQ8"


def connexion_twitter():
    try:
        conn_auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
        conn_auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        return conn_auth
    except Exception as e:
        return None


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = Database()

    return g._database


def initialisation_connexion_hors_flask():
    connection = Database()
    connection.get_connection()

    return connection


def mise_jour_bd():
    print("Maj fait")
    connection = initialisation_connexion_hors_flask()
    liste_contrevenants = recuperation_information_url()

    liste_envoi = []  # Sera utiliser pour l'envoi de courriel
    liste_nom_contrevenant = []  # Sera utiliser pour la section Twitter

    for un_contrevenant in liste_contrevenants:
        liste_champs_xml = initial_champ_importation_xml()
        liste_champs_xml = remplissage_champs_importation_xml(liste_champs_xml,
                                                              un_contrevenant)
        ensemble_existant = connection.verifier_contrevenant_existe(
            liste_champs_xml["proprietaire"], liste_champs_xml["categorie"],
            liste_champs_xml["etablissement"], liste_champs_xml["no_civ"],
            liste_champs_xml["nom_rue"], liste_champs_xml["ville"],
            liste_champs_xml["description"],
            liste_champs_xml["date_infraction"],
            liste_champs_xml["date_jugement"], liste_champs_xml["montant"])
        if len(ensemble_existant) == 0:
            connection.insertion_contrevenant(
                liste_champs_xml["proprietaire"], liste_champs_xml["categorie"],
                liste_champs_xml["etablissement"], liste_champs_xml["no_civ"],
                liste_champs_xml["nom_rue"], liste_champs_xml["ville"],
                liste_champs_xml["description"],
                liste_champs_xml["date_infraction"],
                liste_champs_xml["date_jugement"], liste_champs_xml["montant"])
            liste_envoi.append(liste_champs_xml)
            liste_nom_contrevenant.append(liste_champs_xml["proprietaire"])

    if len(liste_envoi) > 0:
        creation_courriel(liste_envoi)
        conn_auth = connexion_twitter()
        creation_tweet(conn_auth, liste_nom_contrevenant)

    connection.disconnect()


def initial_champ_interval():
    liste_champs = {"date_debut": "", "date_fin": ""}

    return liste_champs


def initial_champ_nouvelle_plainte():
    liste_champs = {"id_plainte": 0, "etablissement": "", "no_civique": 0,
                    "nom_rue": "", "nom_plaignant": "", "description": "",
                    "ville": "", "date_visite": "", "prenom_plaignant": ""}

    return liste_champs


def initial_champ_importation_xml():
    liste_champs_xml = {"proprietaire": "", "categorie": "",
                        "etablissement": "", "no_civ": "", "nom_rue": "",
                        "ville": "", "description": "", "date_infraction": "",
                        "date_jugement": "", "montant": 0}

    return liste_champs_xml


def initial_champ_nouveau_profil():
    liste_champs = {"nom": "", "prenom": "", "courriel": "", "password": "",
                    "liste_etablissement": [], "salt": "", "id_personne": 0,
                    "id_photo": 0}

    return liste_champs


def initial_champ_connexion():
    liste_champs = {"courriel": "", "password": "", "salt": "", "hash": "",
                    "password_hasher": ""}

    return liste_champs


def recuperation_information_url():
    resultat = requests.get(URL)
    resultat.encoding = 'utf-8'
    liste_contrevenants = ET.fromstring(resultat.content)

    return liste_contrevenants


def construction_xml(ensemble_trouve):
    racine = ET.Element('contrevenants')
    for sous_ensemble in ensemble_trouve:
        contrevenant = ET.SubElement(racine, 'contrevenant')
        for cle, valeur in sous_ensemble.items():
            ET.SubElement(contrevenant, cle).text = str(valeur)

    arbre = ET.ElementTree(racine)
    xml_information = BytesIO()
    arbre.write(xml_information, encoding='utf-8', xml_declaration=True)

    return xml_information.getvalue()


def remplissage_champs_importation_xml(liste_champs_xml, contrevenant):
    liste_champs_xml["proprietaire"] = contrevenant.find('proprietaire').text
    liste_champs_xml["categorie"] = contrevenant.find('categorie').text
    liste_champs_xml["etablissement"] = contrevenant.find('etablissement').text
    adresse = contrevenant.find('adresse').text
    # Pour faire optimiser la recherche avec le nom de la rue, je met le
    # numéro civique dans une variable à part
    liste_champs_xml["no_civ"] = adresse.split(' ', 1)[0]
    adresse = adresse.split(' ', 1)[1]
    # Ceci est en raison des données de la ville qui contient un espace après
    # apostrophe ce qui ne sera pas utile lors de recherche d'un nom de rue
    liste_champs_xml["nom_rue"] = adresse.replace("' ", "'")
    liste_champs_xml["ville"] = contrevenant.find('ville').text
    liste_champs_xml["description"] = contrevenant.find('description').text
    liste_champs_xml["date_infraction"] = convertisseur_date(
        contrevenant.find('date_infraction').text)
    liste_champs_xml["date_jugement"] = convertisseur_date(
        contrevenant.find('date_jugement').text)
    montant_en_transformation = contrevenant.find('montant').text.split()
    liste_champs_xml["montant"] = int(montant_en_transformation[0])

    return liste_champs_xml


def remplissage_champs_interval(liste_champs, date_debut, date_fin):
    liste_champs['date_debut'] = date_debut
    liste_champs['date_fin'] = date_fin

    return liste_champs


def convertisseur_date(date_a_convertir):
    date_morceau = date_a_convertir.split()
    jour = date_morceau[0]
    mois = date_morceau[1]
    annee = date_morceau[2]
    dict_mois = {'janvier': '01', 'février': '02', 'mars': '03', 'avril': '04',
                 'mai': '05', 'juin': '06', 'juillet': '07', 'août': '08',
                 'septembre': '09', 'octobre': '10', 'novembre': '11',
                 'décembre': '12'}

    for cle, valeur in dict_mois.items():
        if cle == mois:
            mois = valeur
            break

    nouveau_date = annee + '-' + mois + '-' + jour
    return nouveau_date


def importation_donnees():
    liste_champs_xml = initial_champ_importation_xml()
    liste_contrevenants = recuperation_information_url()
    connection = initialisation_connexion_hors_flask()

    for un_contrevenant in liste_contrevenants:
        liste_champs_xml = remplissage_champs_importation_xml(liste_champs_xml,
                                                              un_contrevenant)
        connection.insertion_contrevenant(
            liste_champs_xml["proprietaire"], liste_champs_xml["categorie"],
            liste_champs_xml["etablissement"], liste_champs_xml["no_civ"],
            liste_champs_xml["nom_rue"], liste_champs_xml["ville"],
            liste_champs_xml["description"],
            liste_champs_xml["date_infraction"],
            liste_champs_xml["date_jugement"], liste_champs_xml["montant"])

    connection.disconnect()


def construction_csv(ensemble_trouve):
    csv_information = StringIO()
    information = csv.writer(csv_information)
    information.writerow(["Etablissement", "Nombre"])
    for sous_ensemble in ensemble_trouve:
        nom_etablissement = ""
        nombre = ""
        for cle, valeur in sous_ensemble.items():
            if cle == "etablissement":
                nom_etablissement = valeur

            elif cle == "nombre":
                nombre = valeur

        information.writerow([nom_etablissement, str(nombre)])

    return csv_information.getvalue()


def initial_champ_recherche():
    liste_champs = {"proprietaire": "", "etablissement": "", "nom_rue": "",
                    "nb_restaurant_trouve": 0, "messages": {}, "nb_critere": 0}

    return liste_champs


def initial_champ_connexion_validation():
    liste_validation = {"situation_erreur": False,
                        "champ_courriel_vide": False,
                        "champ_password_vide": False,
                        "champ_courriel_inv": False,
                        "champ_password_inv": False,
                        "champ_courriel_non_trouve": False,
                        "champ_password_non_trouve": False,
                        "longueur_courriel_inv": False,
                        "longueur_password_inv": False}

    return liste_validation


def initial_champ_recherche_validation():
    liste_validation = {"situation_erreur": False,
                        "champ_proprietaire_vide": False,
                        "champ_etablissement_vide": False,
                        "champ_rue_vide": False,
                        "champs_vides": False,
                        "longueur_proprietaire_inv": False,
                        "longueur_etablissement_inv": False,
                        "longueur_rue_inv": False,
                        "champ_proprietaire_inv": False,
                        "champ_etablissement_inv": False,
                        "champ_rue_inv": False,
                        "aucun_restaurant_trouve": False}

    return liste_validation


def initial_champ_interval_validation():
    liste_validation = {"situation_erreur": False, "champ_debut_inv": False,
                        "champ_fin_inv": False, "champ_debut_vide": False,
                        "champ_fin_vide": False}

    return liste_validation


def remplissage_champ_connexion(request, liste_champs):
    liste_champs['courriel'] = request['courriel']
    liste_champs['password'] = request['password']

    return liste_champs


def remplissage_post_verification_conn(liste_champs, utilisateur):
    liste_champs['salt'] = utilisateur[0]
    liste_champs['hash'] = utilisateur[1]
    liste_champs['password_hasher'] = hashlib.sha512(
        str(liste_champs['password'] + liste_champs['salt']).encode(
            "utf-8")).hexdigest()

    return liste_champs


def remplissage_champ_recherche(request, liste_champs):
    liste_champs['proprietaire'] = request['proprietaire']
    liste_champs['etablissement'] = request['etablissement']
    liste_champs['nom_rue'] = request['nom_rue']

    return liste_champs


def remplissage_champ_nouvelle_plainte(request, liste_champs):
    data = request.get_json()
    liste_champs['etablissement'] = data['etablissement']
    liste_champs['no_civique'] = data['no_civique']
    liste_champs['nom_rue'] = data['nom_rue']
    liste_champs['ville'] = data['ville']
    liste_champs['date_visite'] = data['date_visite']
    liste_champs['prenom_plaignant'] = data['prenom_plaignant']
    liste_champs['nom_plaignant'] = data['nom_plaignant']
    liste_champs['description'] = data['description']

    return liste_champs


def remplissage_champ_nouvelle_profil(request, liste_champs):
    data = request.get_json()
    liste_champs['nom'] = data['nom']
    liste_champs['prenom'] = data['prenom']
    liste_champs['courriel'] = data['courriel']
    liste_champs['password'] = data['password']
    salt = uuid.uuid4().hex
    liste_champs['salt'] = salt
    liste_champs['password'] = hashlib.sha512(
        str(liste_champs['password'] + salt).encode("utf-8")).hexdigest()

    for un_etablissement in data['liste_etablissement']:
        liste_champs['liste_etablissement'].append(un_etablissement)

    return liste_champs


def creation_courriel(liste_envoi):
    string_courriel = recuperation_courriel_yaml()

    message = MIMEMultipart("alternative")
    message["Subject"] = "Voici les nouveaux contrevenants depuis " \
                         "la derniere mise a jour !"
    message["From"] = SOURCE_ADRESSE
    message["To"] = string_courriel
    msg_corps = creation_html_courriel(liste_envoi)
    message.attach(MIMEText(msg_corps, "html"))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(SOURCE_ADRESSE, MOT_DE_PASSE)
    message = message.as_string().encode('utf-8')
    server.sendmail(SOURCE_ADRESSE, string_courriel, message)
    server.quit()


def creation_html_courriel(liste_envoi):
    msg_corps = """<html><head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta charset="utf-8">
        </head><body>
        <h2>Bonjour,</h2>
        <p>Voici la liste des nouveaux contrevenants depuis notre derniere 
        mise a jour pour la ville de Montreal</p>
        <table style="border-collapse: collapse; border: 2px solid black; 
        width: 100%"><thead>
        <tr>
        <th>Propriétaire</th><th>Catégorie</th><th>Établissement</th> 
        <th>No Civique</th><th>Rue</th><th>Ville & Code Postal</th>
        <th>Description</th><th>Date de l'infraction</th>
        <th>Date du jugement</th><th>Montant</th>
        </tr>
        </thead><tbody>    
    """
    for un_etablissement in liste_envoi:
        msg_corps += "<tr>"
        for cle, valeur in un_etablissement.items():
            msg_corps += "<td style=\"border: 1px solid black; padding: 5px; "
            if cle == "montant":
                msg_corps += "text-align: center\">" + str(valeur) + " $</td>"
            elif cle == "description":
                msg_corps += "text-align: justify\">" + valeur + "</td>"
            else:
                msg_corps += "text-align: center\">" + valeur + "</td>"

        msg_corps += "</tr>"

    msg_corps += "</tbody></table>"
    msg_corps += "<p>Bonne journee</p>"
    msg_corps += "</body></html>"

    return msg_corps


def recuperation_courriel_yaml():
    string_courriel = ""
    racine_liste = []
    # Le fichier doit se trouver à la racine du projet
    with open(r'adresse_destination.yaml') as file:
        adresse_list = yaml.full_load(file)
        for item, doc in adresse_list.items():
            racine_liste.append(doc)

    for une_sous_liste in racine_liste:
        for liste_courriel in une_sous_liste:
            string_courriel = liste_courriel

    return string_courriel


def creation_tweet(conn_auth, liste):
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    api = tweepy.API(conn_auth)
    message = "\n\nVoici le nouveau contrevenant prise en " \
              "défault par la ville de Montréal !\n\n"
    for un_contrevenant in liste:
        api.update_status(date + message + un_contrevenant)


def nombre_critiere_recherche(liste_champs):
    nombre = 0

    if len(liste_champs['proprietaire']) != 0:
        nombre += 1

    if len(liste_champs['etablissement']) != 0:
        nombre += 1

    if len(liste_champs['nom_rue']) != 0:
        nombre += 1

    return nombre


"""
 liste_validation = {"situation_erreur": False,
                    "champ_courriel_vide": False,
                    "champ_password_vide": False,
                    "champ_courriel_inv": False,
                    "champ_password_inv": False,
                    "champ_courriel_non_trouve": False,
                    "champ_password_non_trouve": False,
                    "longueur_courriel_inv": False,
                    "longueur_password_inv": False}
"""


def validation_champ_connexion(liste_champs, liste_validation):
    liste_validation = sous_validation_courriel_connexion(liste_champs,
                                                          liste_validation)

    liste_validation = sous_validation_password_connexion(liste_champs,
                                                          liste_validation)

    return liste_validation


def sous_validation_courriel_connexion(liste_champs, liste_validation):
    if liste_champs['courriel'] == "":
        liste_validation['champ_courriel_vide'] = True

    else:
        match_courriel = re.compile(PATTERN_COURRIEL).match
        if match_courriel(liste_champs['courriel']) is None:
            liste_validation['champ_courriel_inv'] = True

        if not (len(liste_champs['courriel']) > 50):
            liste_validation['longueur_courriel_inv'] = True

    return liste_validation


def sous_validation_password_connexion(liste_champs, liste_validation):
    if liste_champs['password'] == "":
        liste_validation['champ_password_vide'] = True

    else:
        match_password = re.compile(PATTERN_PASSWORD).match
        if match_password(liste_champs['password']) is None:
            liste_validation['champ_password_inv'] = True

        if not (8 < len(liste_champs['password']) < 20):
            liste_validation['longueur_password_inv'] = True

    return liste_validation


def validation_champs_interval(liste_champs, liste_validation):
    liste_validation = sous_validation_champs_vide_ajax(liste_champs,
                                                        liste_validation)
    liste_validation = sous_validation_champs_invalide_ajax(liste_champs,
                                                            liste_validation)

    return liste_validation


def sous_validation_champs_vide_ajax(liste_champs, liste_validation):
    if liste_champs['date_debut'] == "":
        liste_validation['champ_debut_vide'] = True

    if liste_champs['date_fin'] == "":
        liste_validation['champ_fin_vide'] = True

    return liste_validation


def sous_validation_champs_invalide_ajax(liste_champs, liste_validation):
    match_date = re.compile(PATTERN_DATE).match
    if not liste_validation['champ_debut_vide']:
        if match_date(liste_champs['date_debut']) is None:
            liste_validation['champ_debut_inv'] = True

    if not liste_validation['champ_fin_vide']:
        if match_date(liste_champs['date_fin']) is None:
            liste_validation['champ_fin_inv'] = True

    return liste_validation


def validation_champs_recherche(liste_champs, liste_validation):
    liste_validation = sous_validation_champs_vide(liste_champs,
                                                   liste_validation)
    liste_validation = sous_validation_champs_longueur(liste_champs,
                                                       liste_validation)
    liste_validation = sous_validation_champs_invalide(liste_champs,
                                                       liste_validation)
    return liste_validation


def sous_validation_champs_vide(liste_champs, liste_validation):
    if liste_champs['proprietaire'] == "":
        liste_validation['champ_proprietaire_vide'] = True

    if liste_champs['etablissement'] == "":
        liste_validation['champ_etablissement_vide'] = True

    if liste_champs['nom_rue'] == "":
        liste_validation['champ_rue_vide'] = True

    if (liste_validation['champ_proprietaire_vide'] and
            liste_validation['champ_etablissement_vide'] and
            liste_validation['champ_rue_vide']):
        liste_validation['champs_vides'] = True

    return liste_validation


def sous_validation_champs_longueur(liste_champs, liste_validation):
    if not liste_validation['champ_proprietaire_vide']:
        if not (5 <= len(liste_champs['proprietaire']) <= 100):
            liste_validation['longueur_proprietaire_inv'] = True

    if not liste_validation['champ_etablissement_vide']:
        if not (5 <= len(liste_champs['etablissement']) <= 65):
            liste_validation['longueur_etablissement_inv'] = True

    if not liste_validation['champ_rue_vide']:
        if not (1 <= len(liste_champs['nom_rue']) <= 35):
            liste_validation['longueur_rue_inv'] = True

    return liste_validation


def sous_validation_champs_invalide(liste_champs, liste_validation):
    if not liste_validation['champ_proprietaire_vide']:
        match_proprio = re.compile(PATTERN_PROPRIO).match
        if match_proprio(liste_champs['proprietaire']) is None:
            liste_validation['champ_proprietaire_inv'] = True

    if not liste_validation['champ_etablissement_vide']:
        match_resto = re.compile(PATTERN_NOM_RESTO).match
        if match_resto(liste_champs['etablissement']) is None:
            liste_validation['champ_etablissement_inv'] = True

    if not liste_validation['champ_rue_vide']:
        match_rue = re.compile(PATTERN_NOM_RUE).match
        if match_rue(liste_champs['nom_rue']) is None:
            liste_validation['champ_rue_inv'] = True

    return liste_validation


def situation_erreur(liste_validation):
    for cle, valeur in liste_validation.items():
        if (cle != "champ_proprietaire_vide" and
                cle != "champ_etablissement_vide" and
                cle != "champ_rue_vide"):
            if valeur:
                liste_validation['situation_erreur'] = True
                # Il n'est pas nécessaire de vérifier
                # si il y a une autre erreur

                break

    return liste_validation


def situation_erreur_interval(liste_validation):
    for cle, valeur in liste_validation.items():
        if valeur:
            liste_validation['situation_erreur'] = True
            break

    return liste_validation


def message_erreur_recherche(liste_validation):
    messages = []
    if liste_validation['champs_vides']:
        messages.append("Vous devez saisir au moins un des trois critères !")

    elif liste_validation['aucun_restaurant_trouve']:
        messages.append("Votre recherche n'a donnée aucun résultats !")

    else:
        messages = sous_message_erreur_proprietaire(messages, liste_validation)
        messages = sous_message_erreur_etablissement(messages,
                                                     liste_validation)
        messages = sous_message_erreur_nom_rue(messages, liste_validation)

    return messages


def sous_message_erreur_proprietaire(messages, liste_validation):
    if liste_validation['champ_proprietaire_inv']:
        messages.append("Attention ! Le nom du propriétaire doit être "
                        "valide !")

    if liste_validation['longueur_proprietaire_inv']:
        messages.append("Attention ! Le nom du propriétaire doit être entre "
                        "5 et 65 caractères !")

    return messages


def sous_message_erreur_etablissement(messages, liste_validation):
    if liste_validation['champ_etablissement_inv']:
        messages.append("Attention ! L'établissement doit être valide !")

    if liste_validation['longueur_etablissement_inv']:
        messages.append("Attention ! Le nom du propriétaire doit être entre "
                        "5 et 100 caractères !")

    return messages


def sous_message_erreur_nom_rue(messages, liste_validation):
    if liste_validation['champ_rue_inv']:
        messages.append("Attention ! Le nom de la rue doit être valide !")

    if liste_validation['longueur_rue_inv']:
        messages.append("Attention ! Le nom de la rue doit être entre "
                        "3 et 35 caractères !")

    return messages
