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

