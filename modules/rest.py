from flask_restful import Resource
from .database import Database  # Importer le fichier database.py
from .fonction import *


class Contrevenant(Resource):
    def get(self, du, au):
        #conn_db = get_db()
        #ensemble_trouve = conn_db.get_restaurant_trouver()
        print(au)