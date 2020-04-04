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

    def liste_tous_restaurants(self):
        cursor = self.get_connection().cursor()
        select = "select distinct etablissement "
        fromm = "from mauvais_restaurants "
        order = "order by etablissement"
        sql = select + fromm + order
        cursor.execute(sql)
        result = cursor.fetchall()
        ensemble_trouve = recuperation_resultat_liste(result)

        return ensemble_trouve

    def liste_restaurant_trouver(self, liste_champs):
        cursor = self.get_connection().cursor()

        liste_critere = remplissage_condition_sql(liste_champs)
        sql = creation_requete_sql(liste_critere, liste_champs['nb_critere'])
        result = execution_requete_dynamique(liste_champs['nb_critere'],
                                             liste_critere, sql, cursor)

        ensemble_trouve = recuperation_resultat(result)

        return ensemble_trouve

    def verifier_contrevenant_existe(self, proprietaire, categorie,
                                     etablissement, no_civ, nom_rue, ville,
                                     description, date_infraction,
                                     date_jugement, montant):
        cursor = self.get_connection().cursor()
        # Le retour du select n'a pas importance comme il ne doit pas avoir de
        # résultat pour l'ajouter dans la BD
        select = "select id_resto "
        fromm = "from mauvais_restaurants "
        where = "where proprietaire = ? and categorie = ?" \
                " and no_civique = ? and nom_rue = ? and ville = ?" \
                " and description = ? and date_infraction = ?" \
                " and date_jugement = ? and montant_amende = ?" \
                " and etablissement = ?"
        sql = select + fromm + where
        cursor.execute(sql, (proprietaire, categorie, no_civ, nom_rue, ville,
                             description, date_infraction, date_jugement,
                             montant, etablissement))
        result = cursor.fetchall()
        return result

    def liste_contrevenant_periode_temps(self, date_debut, date_fin):
        cursor = self.get_connection().cursor()
        select = "select proprietaire, categorie, etablissement, no_civique, " \
                 "nom_rue, ville, description, date_infraction," \
                 "date_jugement, montant_amende, id_resto "
        fromm = "from mauvais_restaurants "
        where = "where date_infraction BETWEEN ? AND ? "
        order = "order by date_infraction "
        sql = select + fromm + where + order
        cursor.execute(sql, (date_debut, date_fin))
        result = cursor.fetchall()
        ensemble_trouve = recuperation_resultat(result)

        return ensemble_trouve

    def nombre_contravention_periode_temps(self, date_debut, date_fin):
        cursor = self.get_connection().cursor()
        select = "select etablissement, count(*) as nombre "
        fromm = "from mauvais_restaurants "
        where = "where date_infraction BETWEEN ? AND ? "
        group = "group by etablissement "
        order = "order by nombre desc, etablissement "
        sql = select + fromm + where + group + order
        cursor.execute(sql, (date_debut, date_fin))
        result = cursor.fetchall()
        ensemble_trouve = recuperation_resultat_regrouper(result)

        return ensemble_trouve


def remplissage_condition_sql(liste_champs):
    # La préparation des critères en vue d'utiliser l'opérateur like aura
    # maintenant une longueur minimale de 2 charactères pour un critère
    # qui aurait été non utiliser par l'Utilisateur
    proprietaire = "%" + liste_champs['proprietaire'] + "%"
    proprietaire = proprietaire.upper()
    etablissement = "%" + liste_champs['etablissement'] + "%"
    etablissement = etablissement.upper()
    nom_rue = "%" + liste_champs['nom_rue'] + "%"

    # Création d'un dictionnaire de critère exclusif
    liste_critere = {"proprietaire": proprietaire,
                     "etablissement": etablissement,
                     "nom_rue": nom_rue}

    return liste_critere


# Le paramètre nb_critere est le nombre de champ qui ne sont pas vide
# lors de la recherche par l'usager. Le paramètre nb_critere_enconstruction est
# une condition à savoir si on doit rajouter ou pas un «AND»
# à la fin de la construction de la section du «WHERE»
# Pour prendre en compte un critere, sa longueur de doit être supérieur
# à 2 comme je prépare dans la fonction remplissage_condition_sql
# les critères de recherches.
def creation_requete_sql(liste_critere, nb_critere):
    select = "select proprietaire, categorie, etablissement, no_civique, " \
             "nom_rue, ville, description, date_infraction," \
             "date_jugement, montant_amende, id_resto "
    fromm = "from mauvais_restaurants "
    where = "where "
    nb_critere_enconstruction = 1
    # Cette section pour la création du where dynamiquement
    for cle, valeur in liste_critere.items():
        if len(valeur) > 2:
            if cle == "proprietaire":
                where += "proprietaire like ? "

            if cle == "etablissement":
                where += "etablissement like ? "

            if cle == "nom_rue":
                where += "nom_rue like ? "

            # Ici, nous savons qu'il reste encore des critères
            if nb_critere_enconstruction < nb_critere:
                where += "and "
                nb_critere_enconstruction += 1

    sql = select + fromm + where

    return sql


# Comme la recherche peut se faire entre 1 à 3 critères donc l'execution
# de la requête peut être dynamique en fonction de l'usager
# Pour prendre en compte un critere, sa longueur de doit être supérieur
# à 2 comme je prépare dans la fonction remplissage_condition_sql
# les critères de recherches.
def execution_requete_dynamique(nb_critere, liste_critere, sql, cursor):
    if nb_critere == 1:
        if len(liste_critere["proprietaire"]) > 2:
            cursor.execute(sql, (liste_critere["proprietaire"],))

        elif len(liste_critere["etablissement"]) > 2:
            cursor.execute(sql, (liste_critere["etablissement"],))

        else:
            cursor.execute(sql, (liste_critere["nom_rue"],))

    elif nb_critere == 2:
        if len(liste_critere["proprietaire"]) > 2 and len(
                liste_critere["etablissement"]) > 2:
            cursor.execute(sql, (liste_critere["proprietaire"],
                                 liste_critere["etablissement"]))

        elif len(liste_critere["proprietaire"]) > 2 and len(
                liste_critere["nom_rue"]) > 2:
            cursor.execute(sql, (liste_critere["proprietaire"],
                                 liste_critere["nom_rue"]))

        else:
            cursor.execute(sql, (liste_critere["etablissement"],
                                 liste_critere["nom_rue"]))
    else:
        cursor.execute(sql, (liste_critere["proprietaire"],
                             liste_critere["etablissement"],
                             liste_critere["nom_rue"]))

    result = cursor.fetchall()

    return result


# Optimisation de la fonction, en changeant l'ensemble pour un tableau
# d'une liste de dictionnaire pour utiliser la même fonction
# pour les taches A2 et A4
def recuperation_resultat(result):
    ensemble_trouve = []
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
            ensemble_trouve.append(sous_ensemble)

    return ensemble_trouve


# Cette fonction sera utiliser pour la tache A5
def recuperation_resultat_regrouper(result):
    ensemble_trouve = []
    if result is not None:
        for un_resto_trouve in result:
            sous_ensemble = {'etablissement': un_resto_trouve[0],
                             'nombre': un_resto_trouve[1]}
            ensemble_trouve.append(sous_ensemble)

    return ensemble_trouve


# Cette fonction sera utiliser pour la tache A6
def recuperation_resultat_liste(result):
    ensemble_trouve = []

    if result is not None:
        for un_resto in result:
            ensemble_trouve.append(un_resto[0])

    return ensemble_trouve
