import time

from flask import Flask

from modules.function import *

import xml.etree.ElementTree as ET
import requests
from datetime import datetime
# Je dois inclure ce package dans la remise du tp

app = Flask(__name__)


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.disconnect()


def importation_donnees():
    resultat = requests.get(URL)
    root = ET.fromstring(resultat.content)

    conn_db = get_db()
    for item in root:
        proprietaire = item.find('proprietaire').text
        categorie = item.find('categorie').text
        etablissement = item.find('etablissement').text
        adresse = item.find('adresse').text
        ville = item.find('ville').text
        description = item.find('description').text
        # Corriger le format de date
        date_infraction = convertisseur_date(item.find('date_infraction').text)
        date_jugement = convertisseur_date(item.find('date_jugement').text)
        montant = item.find('montant').text
        print(date_infraction)


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


def main():
    importation_donnees()


if __name__ == "__main__":
    main()
