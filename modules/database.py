import sqlite3


class Database:
    def __init__(self):
        self.connection = None

    def get_connection(self):
        if self.connection is None:
            # Créer la connexion si elle n'existe pas
            self.connection = sqlite3.connect('db/restaurant.db')

        return self.connection

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()


"""
    # Sera utiliser avec la route /
    def get_articles_recents(self):
        date_auj = date.today()
        cursor = self.get_connection().cursor()
        select = "select auteur, date_publication, identifiant, " \
                 "paragraphe, titre "
        fromm = "from article "
        where = "where date_publication <=? "
        order_by = "order by date_publication desc LIMIT 5"
        sql = select + fromm + where + order_by
        cursor.execute(sql, (date_auj,))
        result = cursor.fetchall()
        # L'ensemble des articles jusqu'à un max de 5 des plus récents
        ensemble = {}
        i = 0
        if result is not None:
            for un_article in result:
                sous_ensemble = {'auteur': un_article[0],
                                 'date_publication': un_article[1],
                                 'identifiant': un_article[2],
                                 'paragraphe': un_article[3],
                                 'titre': un_article[4]}
                ensemble[i] = sous_ensemble
                i += 1

        return ensemble

    # Sera utiliser avec la route /recherche
    def get_articles_trouvees(self, texte):
        cursor = self.get_connection().cursor()
        select = "select titre, date_publication, identifiant "
        fromm = "from article "
        where = "where titre like ? or paragraphe like ? "
        order_by = "order by titre"
        sql = select + fromm + where + order_by
        texte = "%" + texte + "%"
        cursor.execute(sql, (texte, texte))
        result = cursor.fetchall()
        ensemble_trouve = {}
        if result is not None:
            for un_article_trouvee in result:
                sous_ensemble = {'titre': un_article_trouvee[0],
                                 'date_publication': un_article_trouvee[1]}
                ensemble_trouve[un_article_trouvee[2]] = sous_ensemble

        return ensemble_trouve

    # Sera utiliser avec la route /article/<identifiant»
    def get_articles_selectionner(self, identifiant):
        cursor = self.get_connection().cursor()
        select = "select auteur, date_publication, identifiant, " \
                 "paragraphe, titre "
        fromm = "from article "
        where = "where identifiant = ?"
        sql = select + fromm + where
        cursor.execute(sql, (identifiant,))
        result = cursor.fetchone()
        ensemble_trouve = {}

        if result is not None:
            ensemble_trouve = {'auteur': result[0],
                               'date_publication': result[1],
                               'identifiant': result[2],
                               'paragraphe': result[3], 'titre': result[4]}

        return ensemble_trouve

    # Sera utiliser avec la route /admin
    def get_all_articles(self):
        cursor = self.get_connection().cursor()
        select = "select titre, date_publication, identifiant "
        fromm = "from article "
        order_by = "order by titre"
        sql = select + fromm + order_by
        cursor.execute(sql)
        result = cursor.fetchall()
        ensemble = {}
        if result is not None:
            for un_article_trouvee in result:
                sous_ensemble = {'titre': un_article_trouvee[0],
                                 'date_publication': un_article_trouvee[1]}
                ensemble[un_article_trouvee[2]] = sous_ensemble

        return ensemble

    # Sera utiliser avec la route /admin-modif
    def update_article(self, identifiant, titre, paragraphe):
        connection = self.get_connection()
        update_from = "update article "
        update_set = "set titre = ? , paragraphe = ?"
        update_where = "where identifiant = ?"
        sql = update_from + update_set + update_where
        connection.execute(sql, (titre, paragraphe, identifiant))
        connection.commit()

    # Sera utiliser avec la route /admin-nouveau
    def ajouter_article(self, date_publication, titre, paragraphe, identifiant,
                        auteur):
        connection = self.get_connection()
        insert_bd = "insert into article (date_publication, titre, " \
                    "paragraphe, identifiant, auteur) values(?, ?, ?, ?, ?)"
        connection.execute(insert_bd, (
            date_publication, titre, paragraphe, identifiant,
            auteur))
        connection.commit()
"""
