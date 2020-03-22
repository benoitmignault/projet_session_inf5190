from flask import Flask, redirect, render_template, request, session, url_for

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
    if session.get('reset_cookie'):
        session.clear()

    if session.get('titre'):
        titre = session['titre']
    else:
        titre = "Recherche de contrevenant"

    if session.get('erreur_recherche'):
        liste_champs = session['liste_champs']
        liste_validation = session['liste_validation']

    else:
        liste_champs = initial_champ_recherche()
        liste_validation = initial_champ_recherche_validation()

    return render_template('home.html', titre=titre,
                           liste_validation=liste_validation,
                           liste_champs=liste_champs)


@app.route('/recherche_restaurant', methods=["POST"])
def recherche_restaurant():
    liste_champs = initial_champ_recherche()
    liste_validation = initial_champ_recherche_validation()
    liste_champs = remplissage_champ_recherche(request.form, liste_champs)
    liste_champs['nb_critere'] = nombre_critiere_recherche(liste_champs)
    liste_validation = validation_champs_recherche(liste_champs,
                                                   liste_validation)
    conn_db = get_db()
    ensemble_trouve = {}
    if not liste_validation['champs_vides']:
        ensemble_trouve = conn_db.get_restaurant_trouver(liste_champs)
        liste_champs['nb_restaurant_trouve'] = len(ensemble_trouve)
        if liste_champs['nb_restaurant_trouve'] == 0:
            liste_validation['aucun_restaurant_trouve'] = True

    liste_validation = situation_erreur(liste_validation)
    # Utilisation des variables de sessions pour transporter
    # les données nécessaire dans le traitement de la prochaine route
    if liste_validation['situation_erreur']:
        liste_champs['messages'] = message_erreur_recherche(liste_validation)
        session['erreur_recherche'] = True
        # print(liste_validation['situation_erreur'])
        session['liste_champs'] = liste_champs
        session['titre'] = "Problème avec la recherche !"
        session['liste_validation'] = liste_validation
        return redirect(url_for('.home'))

    else:
        session['titre'] = "Recherche réussi !"
        session['ensemble_trouve'] = ensemble_trouve
        session['nb_restaurant_trouve'] = liste_champs['nb_restaurant_trouve']
        return redirect(url_for('.recherche_restaurant_trouve'))


@app.route('/recherche_restaurant_trouve', methods=["GET"])
def recherche_restaurant_trouve():
    # On récupère ici les informations sauvegardées dans la session en cours.
    titre = session['titre']
    ensemble_trouve = session['ensemble_trouve']
    nb_restaurant_trouve = session['nb_restaurant_trouve']
    # Ceci est un indicateur pour détruire les cookies
    # Pour éviter d'avoir de vieux message erreur dans la page accueil
    session['reset_cookie'] = True
    return render_template("recherche_trouve.html", titre=titre,
                           ensemble_trouve=ensemble_trouve,
                           nb_restaurant_trouve=nb_restaurant_trouve)


# Section pour importer directement les informations de la ville via URL.
def main():
    importation_donnees()


if __name__ == "__main__":
    main()

# Creation de la tache A3
