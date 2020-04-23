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

    # Cette fonction sera utilisé pour les taches A1 et A3
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

    # Cette tache sera utilisé pour afficher une liste de tous
    # les établissements un peu partout dans le projet
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

    # Cette fonction sera utilisé pour l»'affichage des établissements
    # trouvé à la recherche faite en A2
    def liste_restaurant_trouver(self, liste_champs):
        cursor = self.get_connection().cursor()

        liste_critere = remplissage_condition_sql(liste_champs)
        sql = creation_requete_sql(liste_critere, liste_champs['nb_critere'])
        result = execution_requete_dynamique(liste_champs['nb_critere'],
                                             liste_critere, sql, cursor)

        ensemble_trouve = recuperation_resultat(result)

        return ensemble_trouve

    # Cette fonction est pour la tache A3 qui a pour but de vérifier
    # si un contrevenant se trouve déjà dans la base de donné
    # Cependant, comme la ville de Montréal n'a pas identifiant unique
    # pour une plainte, la seule manière de vérifier si un contrevenant
    # existe ou pas dans la BD est de mettre toutes ses informations
    # comme conditions dans le WHERE
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

    # Cette fonction est pour la taches A4
    def liste_contravention_interval(self, date_debut, date_fin):
        cursor = self.get_connection().cursor()
        select = "select proprietaire, categorie, etablissement, no_civique, " \
                 "nom_rue, ville, description, date_infraction, " \
                 "date_jugement, montant_amende "
        fromm = "from mauvais_restaurants "
        where = "where date_infraction BETWEEN ? AND ? "
        order = "order by date_infraction "
        sql = select + fromm + where + order
        cursor.execute(sql, (date_debut, date_fin))
        result = cursor.fetchall()
        ensemble_trouve = recuperation_resultat(result)

        return ensemble_trouve

    # Cette fonction est pour la taches A5
    def nombre_contravention_interval(self, date_debut, date_fin):
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

    # Cette fonction est pour les taches C1 à C3
    def nombre_contravention(self):
        cursor = self.get_connection().cursor()
        select = "select etablissement, count(*) as nombre "
        fromm = "from mauvais_restaurants "
        group = "group by etablissement "
        order = "order by nombre desc, etablissement "
        sql = select + fromm + group + order
        cursor.execute(sql)
        result = cursor.fetchall()
        ensemble_trouve = recuperation_resultat_regrouper(result)

        return ensemble_trouve

    # Cette fonction est pour la taches A6
    def liste_contravention_etablissement(self, nom):
        cursor = self.get_connection().cursor()
        select = "select proprietaire, categorie, etablissement, no_civique, " \
                 "nom_rue, ville, description, date_infraction, " \
                 "date_jugement, montant_amende "
        fromm = "from mauvais_restaurants "
        where = "where etablissement = ? "
        order = "order by date_infraction "
        sql = select + fromm + where + order
        cursor.execute(sql, (nom,))
        result = cursor.fetchall()
        ensemble_trouve = recuperation_resultat(result)

        return ensemble_trouve

    # Cette fonction est pour la taches D1
    def inserer_nouvelle_plainte(self, etablissement, no_civique,
                                 nom_rue, ville, date_visite, prenom_plaignant,
                                 nom_plaignant, description):
        connection = self.get_connection()
        insert_bd = "INSERT INTO departement_plaintes " \
                    "(etablissement, no_civique, nom_rue, ville, " \
                    "date_visite, prenom_plaignant, nom_plaignant, " \
                    "description) " \
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        connection.execute(insert_bd,
                           (etablissement, no_civique, nom_rue,
                            ville, date_visite, prenom_plaignant,
                            nom_plaignant, description))
        connection.commit()
        cursor = connection.cursor()
        cursor.execute("select max(id_plainte) from departement_plaintes")
        result = cursor.fetchall()

        return result[0][0]

    # Cette fonction est pour la taches D2
    def verification_existance_plainte(self, id_plainte):
        cursor = self.get_connection().cursor()
        select = "SELECT id_plainte "
        fromm = "FROM departement_plaintes "
        where = "WHERE id_plainte = ? "
        sql = select + fromm + where
        cursor.execute(sql, (id_plainte,))
        result = cursor.fetchall()
        if len(result) is 0:
            return None
        else:
            return result[0][0]

    # Cette fonction est pour la tache E2
    def verification_etablissement_surveiller(self, id_surveillance):
        cursor = self.get_connection().cursor()
        select = "SELECT id_surveillance "
        fromm = "FROM etablissement_surveiller "
        where = "WHERE id_surveillance = ? "
        sql = select + fromm + where
        cursor.execute(sql, (id_surveillance,))
        result = cursor.fetchall()
        if len(result) is 0:
            return None
        else:
            return result[0][0]

    # Cette fonction est pour la tache D2
    def suppression_plainte_existante(self, no_plainte):
        connection = self.get_connection()
        sql = "DELETE from departement_plaintes where id_plainte = ?"
        connection.execute(sql, (no_plainte,))
        connection.commit()

    # Cette fonction est pour la tache E1
    def verification_profil_existant(self, courriel):
        cursor = self.get_connection().cursor()
        select = "SELECT courriel "
        fromm = "FROM profil_utilisateur "
        where = "WHERE courriel = ? "
        sql = select + fromm + where
        cursor.execute(sql, (courriel,))
        result = cursor.fetchall()
        if len(result) is 0:
            return None
        else:
            return result[0][0]

    # Cette fonction est pour la tache E1
    def inserer_nouveau_profil(self, nom, prenom, courriel, password_hasher,
                               salt, liste_etablissement):
        connection = self.get_connection()
        insert_bd = "INSERT INTO profil_utilisateur " \
                    "(nom, prenom, courriel, hash, salt) " \
                    "VALUES (?, ?, ?, ?, ?)"
        connection.execute(insert_bd,
                           (nom, prenom, courriel, password_hasher, salt))
        connection.commit()
        # Maintenant, on va récupérer le id_personne.
        # Ce dernier, il sera utilser pour associer chaque établissement
        # à la personne lors de la création du profil
        cursor = connection.cursor()
        cursor.execute("select max(id_personne) from profil_utilisateur")
        result = cursor.fetchall()
        self.inserer_etablissement_surveiller_profil(result[0][0],
                                                     liste_etablissement)

    # Cette fonction est pour la tache E2
    def inserer_etablissement_surveiller_profil(self, id_personne, liste):
        connection = self.get_connection()
        for un_etablissement in liste:
            insert_bd = "INSERT INTO etablissement_surveiller " \
                        "(id_personne, etablissement) VALUES (?, ?)"
            connection.execute(insert_bd, (id_personne, un_etablissement))
            connection.commit()

    # Cette fonction est pour la tache E2
    def supprimer_etablissement_profil(self, id_personne, id_surveillance):
        connection = self.get_connection()
        delete = "DELETE from etablissement_surveiller "
        where = "where id_personne = ? and id_surveillance = ? "
        sql = delete + where
        connection.execute(sql, (id_personne, id_surveillance))
        connection.commit()

    # Cette fonction est pour la tache E2
    def recuperation_info_connexion(self, courriel):
        cursor = self.get_connection().cursor()
        select = "SELECT salt, hash "
        fromm = "FROM profil_utilisateur "
        where = "WHERE courriel = ? "
        sql = select + fromm + where
        cursor.execute(sql, (courriel,))
        result = cursor.fetchone()
        if result is None:
            return None
        else:
            return result[0], result[1]

    # Cette fonction est pour la tache E2
    def creation_session_active(self, id_session, courriel):
        insert_bd = "INSERT INTO session_profil (id_session, courriel) " \
                    "VALUES (?, ?)"
        connection = self.get_connection()
        connection.execute(insert_bd, (id_session, courriel))
        connection.commit()

    # Cette fonction est pour la tache E2
    def detruire_session_active(self, id_session):
        sql = "DELETE from session_profil where id_session = ?"
        connection = self.get_connection()
        connection.execute(sql, (id_session,))
        connection.commit()

    # Cette fonction est pour la tache E2
    def recuperation_session_active(self, id_session):
        cursor = self.get_connection().cursor()
        select = "SELECT courriel "
        fromm = "FROM session_profil "
        where = "WHERE id_session = ? "
        sql = select + fromm + where
        cursor.execute(sql, (id_session,))
        result = cursor.fetchone()
        if result is None:
            return None
        else:
            return result[0]

    # Cette fonction est pour la tache E2
    def recuperation_profil(self, courriel):
        cursor = self.get_connection().cursor()
        select = "SELECT prenom, nom, id_photo, id_personne, courriel, " \
                 "type_photo "
        fromm = "FROM profil_utilisateur "
        where = "WHERE courriel = ? "
        sql = select + fromm + where
        cursor.execute(sql, (courriel,))
        result = cursor.fetchone()
        if result is None:
            return None
        else:
            return result[0], result[1], result[2], result[3], result[4], \
                   result[5]

    # Cette fonction est pour la tache E2
    def recuperation_profil_etablissement(self, id_personne):
        cursor = self.get_connection().cursor()
        select = "SELECT etablissement, id_surveillance "
        fromm = "FROM etablissement_surveiller "
        where = "WHERE id_personne = ? "
        order = "ORDER BY etablissement "
        sql = select + fromm + where + order
        cursor.execute(sql, (id_personne,))
        result = cursor.fetchall()
        ensemble_trouve = recuperation_liste_etablissement(result)

        return ensemble_trouve

    # Cette fonction est pour la tache E2
    def recuperation_etablissement_restant(self, id_personne):
        cursor = self.get_connection().cursor()
        select1 = "select distinct etablissement "
        from1 = "from mauvais_restaurants "
        where1 = "where etablissement not in "
        sous_request1 = select1 + from1 + where1
        sous_request2 = "( "
        select2 = "select etablissement "
        from2 = "from etablissement_surveiller "
        where2 = "where id_personne = ? "
        sous_request2 += select2 + from2 + where2
        sous_request2 += ") "
        order = "ORDER BY etablissement "
        sql = sous_request1 + sous_request2 + order
        cursor.execute(sql, (id_personne,))
        result = cursor.fetchall()
        ensemble_trouve = recuperation_resultat_liste(result)

        return ensemble_trouve

    # Cette fonction est pour la tache E2
    def ajouter_photo(self, id_photo, fichier):
        connection = self.get_connection()
        connection.execute(
            "insert into photo_utilisateur(id_photo, photo) values(?, ?)",
            [id_photo, sqlite3.Binary(fichier.read())])
        connection.commit()

    # Cette fonction est pour la tache E2
    def recuperer_photo(self, id_photo):
        cursor = self.get_connection().cursor()
        select = "SELECT photo "
        fromm = "from photo_utilisateur "
        where = "where id_photo = ? "
        sql = select + fromm + where
        cursor.execute(sql, (id_photo,))
        picture = cursor.fetchone()
        if picture is None:
            return None
        else:
            blob_data = picture[0]
            return blob_data

    # Cette fonction est pour la tache E2
    def ajout_id_photo_profil(self, id_photo, id_personne, type_photo):
        connection = self.get_connection()
        update = "UPDATE profil_utilisateur "
        sett = "set id_photo = ? , type_photo = ? "
        where = "where id_personne = ? "
        sql = update + sett + where
        connection.execute(sql, (id_photo, type_photo, id_personne))
        connection.commit()

    # Cette fonction est pour la tache E2
    def supprimer_photo_profil(self, id_photo):
        sql = "DELETE from photo_utilisateur where id_photo = ?"
        connection = self.get_connection()
        connection.execute(sql, (id_photo,))
        connection.commit()

    # Cette fonction est pour la tache E2
    def supprimer_lien_photo_profil(self, id_personne):
        connection = self.get_connection()
        update = "UPDATE profil_utilisateur "
        sett = "set id_photo = NULL , type_photo = NULL "
        where = "where id_personne = ? "
        sql = update + sett + where
        connection.execute(sql, (id_personne,))
        connection.commit()

    # Cette fonction est pour la tache E$
    def etablissement_surveiller_par_usager(self, nom_etablissement):
        cursor = self.get_connection().cursor()
        select = "select p.courriel "
        fromm = "from etablissement_surveiller e inner join " \
                "profil_utilisateur p on e.id_personne = p.id_personne "
        where = "where e.etablissement = ? "
        sql = select + fromm + where
        cursor.execute(sql, (nom_etablissement,))
        result = cursor.fetchall()
        liste_courriels = recuperation_liste_courriel(result)
        return liste_courriels

    # Cette fonction sera pour la tache E4
    def ajout_desabonnement_potentiel(self, id_personne, etablissement,
                                      lien_securise, temps_activation):
        connection = self.get_connection()
        update = "UPDATE etablissement_surveiller "
        sett = "set lien_desabonnement = ? , temps_activation_lien = ? "
        where = "where id_personne = ? and etablissement = ? "
        sql = update + sett + where
        connection.execute(sql, (lien_securise, temps_activation, id_personne,
                                 etablissement))
        connection.commit()

    # Cette fonction sera pour la tache E4
    def verif_lien_desabonnement(self, lien_desabonnement):
        cursor = self.get_connection().cursor()
        select = "SELECT etablissement, temps_activation_lien "
        fromm = "FROM etablissement_surveiller "
        where = "WHERE lien_desabonnement = ? "
        sql = select + fromm + where
        cursor.execute(sql, (lien_desabonnement,))
        result = cursor.fetchone()
        if result is None:
            return None
        else:
            return result[0], result[1]


# La préparation des critères en vue d'utiliser l'opérateur like aura
# maintenant une longueur minimale de 2 charactères pour un critère
# qui aurait été non utiliser par l'Utilisateur
def remplissage_condition_sql(liste_champs):
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
             "nom_rue, ville, description, date_infraction, " \
             "date_jugement, montant_amende "
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


# Cette fonction sera pour les taches A2 et A4, A5, A6
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
                             "Montant": un_resto_trouve[9]}
            ensemble_trouve.append(sous_ensemble)

    return ensemble_trouve


# Cette fonction sera utiliser pour la tache A5 et C1 à C3
def recuperation_resultat_regrouper(result):
    ensemble_trouve = []
    if result is not None:
        for un_resto_trouve in result:
            sous_ensemble = {'etablissement': un_resto_trouve[0],
                             'nombre': un_resto_trouve[1]}
            ensemble_trouve.append(sous_ensemble)

    return ensemble_trouve


# Cette fonction sera utiliser pour la tache A6, E2
def recuperation_resultat_liste(result):
    ensemble_trouve = []

    if result is not None:
        for un_resto in result:
            ensemble_trouve.append(un_resto[0])

    return ensemble_trouve


# Cette fonction sera utilser pour la tache E2
def recuperation_liste_etablissement(result):
    ensemble_trouve = []
    if result is not None:
        for un_etablissement in result:
            sous_ensemble = {'nom': un_etablissement[0],
                             'id_surveillance': un_etablissement[1]}
            ensemble_trouve.append(sous_ensemble)

    return ensemble_trouve


# Cette fonction sera pour E3
def recuperation_liste_courriel(result):
    liste_courriels = []
    if result is not None:
        for un_etablissement in result:
            liste_courriels.append(un_etablissement[0])

    return liste_courriels
