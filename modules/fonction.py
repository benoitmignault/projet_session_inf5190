import xml.etree.ElementTree as ET
import re  # pour la gestion des patterns pour les différents champs input

from flask import g

import requests

from .database import Database  # Importer le fichier database.py

# Lien qui sera utilisé pour récupérer les informations
URL = 'http://donnees.ville.montreal.qc.ca/dataset/a5c1f0b9-261f-4247-99d8-' \
      'f28da5000688/resource/92719d9b-8bf2-4dfd-b8e0-1021ffcaee2f/download/' \
      'inspection-aliments-contrevenants.xml'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = Database()

    return g._database


def initial_champ_importation_xml():
    liste_champs_xml = {"proprietaire": "", "categorie": "",
                        "etablissement": "",
                        "adresse": "", "ville": "", "description": "",
                        "date_infraction": "", "date_jugement": "",
                        "montant": 0}

    return liste_champs_xml


def remplissage_champs_xml(liste_champs_xml, un_contrevenant):
    liste_champs_xml['proprietaire'] = un_contrevenant.find('proprietaire').text
    liste_champs_xml['categorie'] = un_contrevenant.find('categorie').text
    liste_champs_xml['etablissement'] = un_contrevenant.find(
        'etablissement').text
    adresse = un_contrevenant.find('adresse').text
    # Ceci est en raison des données de la ville qui contient un espace après
    # apostrophe ce qui ne sera pas utile lors de recherche d'un nom de rue
    liste_champs_xml['adresse'] = adresse.replace("' ", "'")
    liste_champs_xml['ville'] = un_contrevenant.find('ville').text
    liste_champs_xml['description'] = un_contrevenant.find('description').text
    liste_champs_xml['date_infraction'] = convertisseur_date(
        un_contrevenant.find('date_infraction').text)
    liste_champs_xml['date_jugement'] = convertisseur_date(
        un_contrevenant.find('date_jugement').text)
    montant_en_transformation = un_contrevenant.find('montant').text.split()
    liste_champs_xml['montant'] = int(montant_en_transformation[0])

    return liste_champs_xml


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

    resultat = requests.get(URL)
    resultat.encoding = 'utf-8'
    liste_contrevenants = ET.fromstring(resultat.content)

    connection = Database()
    connection.get_connection()
    for un_contrevenant in liste_contrevenants:
        liste_champs_xml = remplissage_champs_xml(liste_champs_xml,
                                                  un_contrevenant)
        connection.insertion_contrevenant(liste_champs_xml['proprietaire'],
                                          liste_champs_xml['categorie'],
                                          liste_champs_xml['etablissement'],
                                          liste_champs_xml['adresse'],
                                          liste_champs_xml['ville'],
                                          liste_champs_xml['description'],
                                          liste_champs_xml['date_infraction'],
                                          liste_champs_xml['date_jugement'],
                                          liste_champs_xml['montant'])

    connection.disconnect()


def initial_champ_recherche():
    liste_champs = {"proprietaire": "", "etablissement": "", "rue": ""}

    return liste_champs


def initial_champ_recherche_validation():
    liste_validation_admin = {"situation_erreur": False,
                              "champ_proprietaire_vide": False,
                              "champ_etablissement_vide": False,
                              "champ_rue_vide": False,
                              "champs_vides": False,
                              "longueur_proprietaire_inv": False,
                              "longueur_etablissement_inv": False,
                              "longueur_rue_inv": False,
                              "champ_proprietaire_inv": False,
                              "champ_etablissement_inv": False,
                              "champ_rue_inv": False}

    return liste_validation_admin


def validation_champs_recherche(liste_champs, liste_validation):
    if liste_champs['recher_article'] == "":
        liste_validation['champ_recher_article_vide'] = True

    return liste_validation



# J'ai décidé de séparer mes fonction de remplissages
# comme ce n'est pas les mêmes champs qui seront utilisés
# Fonction utiliser lors de modification articles
# liste_champs représente ceux du fichier index.py liste_champs_admin
def remplissage_champs_modif_article(request, liste_champs):
    liste_champs['titre'] = request.form['nom_article']
    # Je dois utiliser strip pour retirer les retours de lignes non nécessaire
    liste_champs['paragraphe'] = request.form['nom_paragraphe'].strip()
    liste_champs['identifiant'] = request.form['identifiant']
    liste_champs['auteur'] = request.form['nom_auteur']
    liste_champs['date_publication'] = request.form['date_publication']
    liste_champs['titre_avant'] = request.form['nom_article_avant']
    liste_champs['paragraphe_avant'] = request.form['nom_paragraphe_avant']

    return liste_champs


# Fonction utiliser lors d'ajout les articles
# liste_champs représente ceux du fichier index.py liste_champs_admin
def remplissage_champs_ajout_article(request, liste_champs):
    liste_champs['date_publication'] = request.form['date']
    liste_champs['titre'] = request.form['nom_article']
    # Je dois utiliser strip pour retirer les retours de lignes non nécessaire
    liste_champs['paragraphe'] = request.form['nom_paragraphe'].strip()
    liste_champs['identifiant'] = request.form['identifiant']
    liste_champs['auteur'] = request.form['nom_auteur']

    return liste_champs


# liste_champs représente ceux du fichier index.py liste_champs_admin
# liste_validation représente ceux du fichier index.py liste_validation_admin
# Le but était de simpliment aléger la lourdeur du code
def validation_champs_article(liste_champs, liste_validation):
    liste_validation = validation_titre(liste_champs['titre'],
                                        liste_validation)
    liste_validation = validation_paragraphe(liste_champs['paragraphe'],
                                             liste_validation)
    liste_validation = validation_date(liste_champs['date_publication'],
                                       liste_validation)
    liste_validation = validation_identifiant(liste_champs['identifiant'],
                                              liste_validation)
    liste_validation = validation_auteur(liste_champs['auteur'],
                                         liste_validation)

    # Validation si on a au moins un champ vide
    if (liste_validation['champ_titre_vide'] or
            liste_validation['champ_paragraphe_vide'] or
            liste_validation['champ_date_vide'] or
            liste_validation['champ_identifiant_vide'] or
            liste_validation['champ_auteur_vide']):
        liste_validation['champs_vides'] = True

    if not liste_validation['champs_vides']:
        # Seulement si les champs ne sont pas vide,
        # qu'on va poursuivre les validations de manière logique
        if liste_champs['paragraphe'] == liste_champs['paragraphe_avant']:
            liste_validation['champ_paragraphe_pareil'] = True

        if liste_champs['titre'] == liste_champs['titre_avant']:
            liste_validation['champ_titre_pareil'] = True

        if liste_validation['champ_paragraphe_pareil'] and \
                liste_validation['champ_titre_pareil']:
            liste_validation['aucune_modification'] = True
            # On calcul les validités sur les longueurs des champs

    return liste_validation


def validation_titre(titre, liste_validation):
    if titre == "":
        liste_validation['champ_titre_vide'] = True

    else:
        if not (3 <= len(titre) <= 15):
            liste_validation['longueur_titre_inv'] = True

        match_titre = re.compile(PATTERN_TITRE).match
        if match_titre(titre) is None:
            liste_validation['champ_titre_inv'] = True

    return liste_validation


def validation_paragraphe(paragraphe, liste_validation):
    if paragraphe == "":
        liste_validation['champ_paragraphe_vide'] = True

    else:
        if not (10 <= len(paragraphe) <= 100):
            liste_validation['longueur_paragraphe_inv'] = True

        match_paragraphe = re.compile(PATTERN_PARAGRAPHE).match
        if match_paragraphe(paragraphe) is None:
            liste_validation['champ_paragraphe_inv'] = True

    return liste_validation


def validation_date(date, liste_validation):
    if date == "":
        liste_validation['champ_date_vide'] = True
    else:
        if not (len(date) == 10):
            liste_validation['longueur_date_inv'] = True

        match_date = re.compile(PATTERN_DATE).match
        if match_date(date) is None:
            liste_validation['champ_date_inv'] = True

    return liste_validation


def validation_identifiant(identifiant, liste_validation):
    if identifiant == "":
        liste_validation['champ_identifiant_vide'] = True

    else:
        if not (3 <= len(identifiant) <= 15):
            liste_validation['longueur_identifiant_inv'] = True

        match_identifiant = re.compile(PATTERN_IDENTIFIANT).match
        if match_identifiant(identifiant) is None:
            liste_validation['champ_identifiant_inv'] = True

    return liste_validation


def validation_auteur(auteur, liste_validation):
    if auteur == "":
        liste_validation['champ_auteur_vide'] = True

    else:
        if not (3 <= len(auteur) <= 15):
            liste_validation['longueur_auteur_inv'] = True

        match_auteur = re.compile(PATTERN_AUTEUR).match
        if match_auteur(auteur) is None:
            liste_validation['champ_auteur_inv'] = True

    return liste_validation


# L'indicateur pour savoir si on continu ou
# si on arrête se que nous sommes entrains de faire
def situation_erreur(liste_validation):
    for cle, valeur in liste_validation.items():
        if valeur:
            liste_validation['situation_erreur'] = True

    return liste_validation


def message_erreur(liste_validation):
    messages = {}
    if liste_validation["champ_recher_article_vide"]:
        messages['champ_vide'] = \
            "Le champ ne peut rester vide si vous voulez faire une recherche !"

    if liste_validation["aucun_article_trouve"]:
        messages['zero_article_trouve'] = \
            "Le texte utilisé pour la recherche n'a " \
            "donné aucun article trouvé !"

    if liste_validation["aucun_article_recent"]:
        messages['zero_article_recent'] = \
            "Aucun article est en date du jour dans l'inventaire !"

    if liste_validation["aucun_article"]:
        messages['aucun_article'] = \
            "Aucun article a été enregistré dans l'inventaire !"

    return messages


def message_erreur_admin(liste_validation):
    messages = []
    if liste_validation['champ_titre_vide']:
        messages.append("Le nouveau titre de l'article ne peut être vide !")

    if liste_validation['champ_paragraphe_vide']:
        messages.append(
            "Le nouveau paragraphe de l'article ne peut être vide !")

    if liste_validation['aucune_modification']:
        messages.append(
            "Vous devez modifier au moins l'un des "
            "champs suivant : Titre ou Paragraphe !")

    if liste_validation['update_reussi']:
        messages.append("La mise à jour de l'article a été un succès !")

    return messages


def message_erreur_admin_ajout(liste_validation):
    messages = []
    if liste_validation['ajout_reussi']:
        messages.append("L'ajout de l'article a fonctionné !")
    else:
        messages = message_erreur_titre(messages, liste_validation)
        messages = message_erreur_auteur(messages, liste_validation)
        messages = message_erreur_paragraphe(messages, liste_validation)
        messages = message_erreur_identifiant(messages, liste_validation)

    return messages


def message_erreur_titre(messages, liste_validation):
    if liste_validation['champ_titre_vide']:
        messages.append("Attention ! Le titre ne peut être vide !")

    if liste_validation['longueur_titre_inv']:
        messages.append(
            "Attention ! Le titre de l'article "
            "doit être entre 3 et 15 caractères !")

    if liste_validation['champ_titre_inv']:
        messages.append("Attention ! le titre de l'article n'est pas valide !")

    return messages


def message_erreur_auteur(messages, liste_validation):
    if liste_validation['champ_auteur_vide']:
        messages.append(
            "Attention ! Un article doit être associer à un auteur !")

    if liste_validation['champ_auteur_inv']:
        messages.append("Attention ! le nom de l'auteur n'est pas valide !")

    if liste_validation['longueur_auteur_inv']:
        messages.append(
            "Attention ! L'auteur de l'article doit "
            "être entre 3 et 15 caractères !")

    return messages


def message_erreur_paragraphe(messages, liste_validation):
    if liste_validation['champ_paragraphe_vide']:
        messages.append("Attention ! Le paragraphe  ne peut être vide !")

    if liste_validation['longueur_paragraphe_inv']:
        messages.append(
            "Attention ! La longueur du paragraphe doit être "
            "entre 10 et 100 caractères !")

    if liste_validation['champ_paragraphe_inv']:
        messages.append(
            "Attention ! le contenu du paragraphe de l'article "
            "n'est pas valide !")

    return messages


def message_erreur_identifiant(messages, liste_validation):
    if liste_validation['identifiant_deja_prise']:
        messages.append(
            "Attention ! L'identifiant existe déjà, veuiller "
            "en choisir un autre !")

    if liste_validation['champ_identifiant_vide']:
        messages.append("Attention ! Le identifiant ne peut être vide !")

    if liste_validation['longueur_identifiant_inv']:
        messages.append(
            "Attention ! L'identifiant doit être entre 3 et 15 caractères !")

    if liste_validation['champ_identifiant_inv']:
        messages.append(
            "Attention ! l'identifiant unique pour "
            "l'article n'est pas valide !")

    return messages


def message_erreur_date(messages, liste_validation):
    if liste_validation['champ_date_vide']:
        messages.append(
            "Attention ! La date de publication ne peut être vide !")

    if liste_validation['champ_date_inv']:
        messages.append(
            "Attention ! La date saisie n'est pas valide selon "
            "le format «AAAA-MM-DD» !")

    if liste_validation['longueur_date_inv']:
        messages.append(
            "Attention ! L'identifiant doit avoir 10 caractères "
            "pas plus pas moins !")

    return messages
