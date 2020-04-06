import xmlify
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.combining import OrTrigger
from apscheduler.triggers.cron import CronTrigger
from flask import Flask, jsonify, redirect, render_template, request, session, \
    url_for, Response

from modules.fonction import *

app = Flask(__name__, static_url_path='', static_folder='static')

# Déclaration de la secret key pour me permettre utiliser
# les variables de sessions
app.secret_key = "(*&*&322387he738220)(*(*22347657"


@app.errorhandler(404)
def not_found(e):
    erreur_404 = True
    titre = "Page inexistante - 404"
    return render_template("erreur_404.html", titre=titre,
                           erreur_404=erreur_404)


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

    conn_db = get_db()
    liste_etablissement = conn_db.liste_tous_restaurants()

    return render_template('home.html', titre=titre,
                           liste_etablissement=liste_etablissement,
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
        ensemble_trouve = conn_db.liste_restaurant_trouver(liste_champs)
        liste_champs['nb_restaurant_trouve'] = len(ensemble_trouve)
        if liste_champs['nb_restaurant_trouve'] == 0:
            liste_validation['aucun_restaurant_trouve'] = True

    else:
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


# Tache A3
scheduler = BackgroundScheduler(daemon=True)
trigger = OrTrigger([CronTrigger(day_of_week='*', hour=0, minute=0)])

scheduler.add_job(mise_jour_bd, trigger)
scheduler.start()


# Deuxième partie de A4 sera de créer une documentation RAML
@app.route('/api/contrevenants/du=<date_debut>&au=<date_fin>',
           methods=["GET", "POST"])
def recherche_contrevenants_interval(date_debut, date_fin):
    liste_champs_interval = initial_champ_interval()
    liste_validation_interval = initial_champ_interval_validation()
    liste_champs_interval = remplissage_champs_interval(liste_champs_interval,
                                                        date_debut, date_fin)
    liste_validation_interval = validation_champs_interval(
        liste_champs_interval, liste_validation_interval)
    liste_validation_interval = situation_erreur_interval(
        liste_validation_interval)

    ensemble_trouve = []
    if not liste_validation_interval['situation_erreur']:
        conn_db = get_db()

        if request.method == "GET":
            ensemble_trouve = conn_db.liste_contrevenant_interval(
                liste_champs_interval['date_debut'],
                liste_champs_interval['date_fin'])

        elif request.method == "POST":
            ensemble_trouve = conn_db.nombre_contravention_interval(
                liste_champs_interval['date_debut'],
                liste_champs_interval['date_fin'])

        return jsonify(ensemble_trouve)

    else:
        titre = "Erreur Système - 400"
        erreur_400 = True
        return render_template('erreur_400.html', titre=titre,
                               erreur_400=erreur_400), 400


# Cette fonction était pour la tache A6
@app.route(
    '/api/contrevenant/du=<date_debut>&au=<date_fin>&etablissement=<nom>',
    methods=["GET"])
def recherche_liste_contravention_par_etablissement(date_debut, date_fin, nom):
    liste_champs_etablissement = initial_champ_etablissement()
    liste_validation_etablissement = initial_champ_etablissement_validation()
    liste_champs_etablissement = remplissage_champs_etablissement(
        liste_champs_etablissement,
        date_debut, date_fin, nom)
    liste_validation_etablissement = validation_champs_etablissement(
        liste_champs_etablissement, liste_validation_etablissement)
    liste_validation_etablissement = situation_erreur_interval(
        liste_validation_etablissement)

    if not liste_validation_etablissement['situation_erreur']:
        conn_db = get_db()

        ensemble_trouve = conn_db.liste_contravention_etablissement(
            liste_champs_etablissement['date_debut'],
            liste_champs_etablissement['date_fin'],
            liste_champs_etablissement['etablissement'])

        return jsonify(ensemble_trouve)

    else:
        titre = "Erreur Système - 400"
        erreur_400 = True
        return render_template('erreur_400.html', titre=titre,
                               erreur_400=erreur_400), 400


# Cette fonction était pour la tache C1
@app.route('/api/contrevenants/json', methods=["GET"])
def recherche_contrevenants_json():
    conn_db = get_db()
    ensemble_trouve = conn_db.nombre_contravention()

    return jsonify(ensemble_trouve)


# Cette fonction était pour la tache C2
@app.route('/api/contrevenants/xml', methods=["GET"])
def recherche_contrevenants_xml():
    conn_db = get_db()
    ensemble_trouve = conn_db.nombre_contravention()
    xml_information = construction_xml(ensemble_trouve)

    return Response(xml_information, mimetype='text/xml')


def main():
    importation_donnees()


# Cette fonction était pour la tache A1
if __name__ == "__main__":
    main()
