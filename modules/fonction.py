import csv
import re  # pour la gestion des patterns pour les différents champs input
import xml.etree.ElementTree as ET
from io import BytesIO, StringIO

import requests
from flask import g

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


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = Database()

    return g._database


# Fonction pour création la connexion qui sera utilisé dans un contexte hors
# d'une route utilisée avec Flask
def initialisation_connexion_hors_flask():
    connection = Database()
    connection.get_connection()

    return connection


def mise_jour_bd():
    liste_champs_xml = initial_champ_importation_xml()
    liste_contrevenants = recuperation_information_url()
    connection = initialisation_connexion_hors_flask()

    for un_contrevenant in liste_contrevenants:

        liste_champs_xml = remplissage_champs_importation_xml(liste_champs_xml,
                                                              un_contrevenant)
        ensemble_existant = connection.verifier_contrevenant_existe(
            liste_champs_xml['proprietaire'],
            liste_champs_xml['categorie'],
            liste_champs_xml['etablissement'],
            liste_champs_xml['no_civ'],
            liste_champs_xml['nom_rue'],
            liste_champs_xml['ville'],
            liste_champs_xml['description'],
            liste_champs_xml['date_infraction'],
            liste_champs_xml['date_jugement'],
            liste_champs_xml['montant'])
        if len(ensemble_existant) == 0:
            connection.insertion_contrevenant(
                liste_champs_xml['proprietaire'],
                liste_champs_xml['categorie'],
                liste_champs_xml['etablissement'],
                liste_champs_xml['no_civ'],
                liste_champs_xml['nom_rue'],
                liste_champs_xml['ville'],
                liste_champs_xml['description'],
                liste_champs_xml['date_infraction'],
                liste_champs_xml['date_jugement'],
                liste_champs_xml['montant'])

    connection.disconnect()


def initial_champ_interval():
    liste_champs = {"date_debut": "", "date_fin": ""}

    return liste_champs


def initial_champ_importation_xml():
    liste_champs_xml = {"proprietaire": "", "categorie": "",
                        "etablissement": "", "no_civ": "", "nom_rue": "",
                        "ville": "", "description": "", "date_infraction": "",
                        "date_jugement": "", "montant": 0}

    return liste_champs_xml


# Fonction pour récupérer les informations venant de URL
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


def remplissage_champs_importation_xml(liste_champs_xml, un_contrevenant):
    liste_champs_xml['proprietaire'] = un_contrevenant.find('proprietaire').text
    liste_champs_xml['categorie'] = un_contrevenant.find('categorie').text
    liste_champs_xml['etablissement'] = un_contrevenant.find(
        'etablissement').text
    adresse = un_contrevenant.find('adresse').text
    # Pour faire optimiser la recherche avec le nom de la rue, je met le
    # numéro civique dans une variable à part
    liste_champs_xml['no_civ'] = adresse.split(' ', 1)[0]
    adresse = adresse.split(' ', 1)[1]
    # Ceci est en raison des données de la ville qui contient un espace après
    # apostrophe ce qui ne sera pas utile lors de recherche d'un nom de rue
    liste_champs_xml['nom_rue'] = adresse.replace("' ", "'")
    liste_champs_xml['ville'] = un_contrevenant.find('ville').text
    liste_champs_xml['description'] = un_contrevenant.find('description').text
    liste_champs_xml['date_infraction'] = convertisseur_date(
        un_contrevenant.find('date_infraction').text)
    liste_champs_xml['date_jugement'] = convertisseur_date(
        un_contrevenant.find('date_jugement').text)
    montant_en_transformation = un_contrevenant.find('montant').text.split()
    liste_champs_xml['montant'] = int(montant_en_transformation[0])

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
        connection.insertion_contrevenant(liste_champs_xml['proprietaire'],
                                          liste_champs_xml['categorie'],
                                          liste_champs_xml['etablissement'],
                                          liste_champs_xml['no_civ'],
                                          liste_champs_xml['nom_rue'],
                                          liste_champs_xml['ville'],
                                          liste_champs_xml['description'],
                                          liste_champs_xml['date_infraction'],
                                          liste_champs_xml['date_jugement'],
                                          liste_champs_xml['montant'])

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


def remplissage_champ_recherche(request, liste_champs):
    liste_champs['proprietaire'] = request['proprietaire']
    liste_champs['etablissement'] = request['etablissement']
    liste_champs['nom_rue'] = request['nom_rue']

    return liste_champs


def nombre_critiere_recherche(liste_champs):
    nombre = 0

    if len(liste_champs['proprietaire']) != 0:
        nombre += 1

    if len(liste_champs['etablissement']) != 0:
        nombre += 1

    if len(liste_champs['nom_rue']) != 0:
        nombre += 1

    return nombre


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
                # Il n'est pas nécessaire de vérifier si il y a une autre erreur
                # de validation à true.
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
        messages = sous_message_erreur_etablissement(messages, liste_validation)
        messages = sous_message_erreur_nom_rue(messages, liste_validation)

    return messages


def sous_message_erreur_proprietaire(messages, liste_validation):
    if liste_validation['champ_proprietaire_inv']:
        messages.append("Attention ! Le nom du propriétaire doit être valide !")

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
