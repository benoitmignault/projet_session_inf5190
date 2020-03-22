import sqlite3


class Database:

    def __init__(self):
        self.connection = None

    def get_connection(self):
        if self.connection is None:
            # Créer la BD si elle n'existe pas
            self.connection = sqlite3.connect('db/restaurant.db')

        return self.connection

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()

    def insertion_contrevenant(self, proprietaire, categorie, etablissement,
                               no_civ, nom_rue, ville, description,
                               date_infraction, date_jugement, montant):

        insert_bd = "INSERT INTO mauvais_restaurants (proprietaire, " \
                    "categorie, etablissement, no_civique, nom_rue, ville," \
                    "description, date_infraction, date_jugement," \
                    "montant_amende) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        self.connection.execute(insert_bd,
                                (proprietaire, categorie, etablissement,
                                 no_civ, nom_rue, ville, description,
                                 date_infraction, date_jugement, montant))
        self.connection.commit()

    def get_restaurant_trouver(self, liste_champs):
        cursor = self.get_connection().cursor()
        select = "select proprietaire, categorie, etablissement, no_civique, " \
                 "nom_rue, ville, description, date_infraction," \
                 "date_jugement, montant_amende, id_resto "
        fromm = "from mauvais_restaurants "
        where = "where "
        nb_critere = 1
        # Création d'un dictionnaire de critère exclusif
        liste_critere = {"proprietaire": liste_champs['proprietaire'],
                         "etablissement": liste_champs['etablissement'],
                         "nom_rue": liste_champs['nom_rue']}

        # Cette section pour la création du where dynamiquement
        for cle, valeur in liste_critere.items():
            if len(valeur) != 0:
                if cle == "proprietaire":
                    where += "proprietaire like ? "

                if cle == "etablissement":
                    where += "etablissement like ? "

                if cle == "nom_rue":
                    where += "nom_rue like ? "

                # Ici, nous savons qu'il reste encore des critères
                if nb_critere < liste_champs['nb_critere']:
                    where += "and "
                    nb_critere += 1

        sql = select + fromm + where
        proprietaire = "%" + liste_critere['proprietaire'] + "%"
        proprietaire = proprietaire.upper()
        etablissement = "%" + liste_critere['etablissement'] + "%"
        etablissement = etablissement.upper()
        nom_rue = "%" + liste_critere['nom_rue'] + "%"

        if liste_champs['nb_critere'] == 1:
            if len(liste_critere["proprietaire"]) != 0:
                cursor.execute(sql, (proprietaire,))

            elif len(liste_critere["etablissement"]) != 0:
                cursor.execute(sql, (etablissement,))

            else:
                cursor.execute(sql, (nom_rue,))

        elif liste_champs['nb_critere'] == 2:
            if len(liste_critere["proprietaire"]) != 0 and len(
                    liste_critere["etablissement"]) != 0:
                cursor.execute(sql, (proprietaire, etablissement))

            elif len(liste_critere["proprietaire"]) != 0 and len(
                    liste_critere["nom_rue"]) != 0:
                cursor.execute(sql, (proprietaire, nom_rue))

            else:
                cursor.execute(sql, (etablissement, nom_rue))

        else:
            cursor.execute(sql, (proprietaire, etablissement, nom_rue))

        result = cursor.fetchall()
        ensemble_trouve = {}
        if result is not None:
            for un_resto_trouve in result:
                sous_ensemble = {'Propriétaire': un_resto_trouve[0],
                                 'Catégorie': un_resto_trouve[1],
                                 'Établissement': un_resto_trouve[2],
                                 'Adresse':
                                     un_resto_trouve[3] + " " +
                                     un_resto_trouve[4],
                                 'Ville': un_resto_trouve[5],
                                 'Description': un_resto_trouve[6],
                                 "Date d'infraction": un_resto_trouve[7],
                                 'Date de jugement': un_resto_trouve[8],
                                 "Montant de l'amende": un_resto_trouve[9]}
                ensemble_trouve[un_resto_trouve[10]] = sous_ensemble

        return ensemble_trouve
