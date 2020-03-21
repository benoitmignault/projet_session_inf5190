from flask import Flask, render_template

from modules.fonction import *

app = Flask(__name__, static_url_path='', static_folder='static')

# Déclaration de la secret key pour me permettre utiliser
# les variables de sessions
app.secret_key = "(*&*&322387he738220)(*(*22347657"


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)

    if db is not None:
        db.disconnect()


@app.route('/', methods=["GET"])
def home():
    titre = "Recherche de contrevenant"

    liste_champs = initial_champ_recherche()
    liste_validation = initial_champ_recherche_validation()

    return render_template('home.html', titre=titre,
                           liste_validation=liste_validation,
                           liste_champs=liste_champs)


# Section pour importer directement les informations de la ville via URL.
def main():
    importation_donnees()


if __name__ == "__main__":
    main()
