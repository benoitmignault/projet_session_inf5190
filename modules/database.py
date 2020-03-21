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
                               adresse, ville, description, date_infraction,
                               date_jugement, montant):

        insert_bd = "INSERT INTO mauvais_restaurants (proprietaire, categorie, " \
                    "etablissement, adresse, ville, description, " \
                    "date_infraction, date_jugement, montant_amende) " \
                    "VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)"
        self.connection.execute(insert_bd,
                                (proprietaire, categorie, etablissement,
                                 adresse, ville, description, date_infraction,
                                 date_jugement, montant))
        self.connection.commit()
