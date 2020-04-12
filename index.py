from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.combining import OrTrigger
from apscheduler.triggers.cron import CronTrigger
from flask import Flask, Response, jsonify, redirect
from flask import render_template, request, session, url_for
from flask_json_schema import JsonSchema
from flask_json_schema import JsonValidationError

from modules.fonction import *
from validateur_plainte_json_schema import nouvelle_plainte_etablissement
from validateur_profil_json_schema import nouveau_profil

app = Flask(__name__, static_url_path='', static_folder='static')
schema = JsonSchema(app)
# Déclaration de la secret key pour me permettre utiliser
# les variables de sessions
app.secret_key = "(*&*&322387he738220)(*(*22347657"


@app.errorhandler(404)
def not_found(e):
    erreur_404 = True
    titre = "Page inexistante - 404"
    return render_template("erreur_404.html", titre=titre,
                           erreur_404=erreur_404)


@app.errorhandler(JsonValidationError)
def validation_error(erreur):
    errors = [validation.message for validation in erreur.errors]
    return jsonify({"Le champ en problème": erreur.message,
                    "Le message d'erreur": errors}), 400


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)

    if db is not None:
        db.disconnect()


@app.route('/doc')
def documentation():
    return render_template('doc.html')


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
trigger = OrTrigger([CronTrigger(day_of_week='*', hour=9, minute=17)])

scheduler.add_job(mise_jour_bd, trigger)
scheduler.start()


# Cette fonction est pour la route A4 et A5
@app.route('/api/nombre_amende_etablissement/interval', methods=["GET"])
def recherche_contrevenants_interval():
    liste_champs_interval = initial_champ_interval()
    liste_validation_interval = initial_champ_interval_validation()
    liste_champs_interval = remplissage_champs_interval(liste_champs_interval,
                                                        request.args["du"],
                                                        request.args["au"])
    liste_validation_interval = validation_champs_interval(
        liste_champs_interval, liste_validation_interval)
    liste_validation_interval = situation_erreur_interval(
        liste_validation_interval)

    if not liste_validation_interval['situation_erreur']:
        conn_db = get_db()
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
@app.route('/api/liste_amendes_etablissement/etablissement', methods=["GET"])
def recherche_liste_contravention_par_etablissement():
    if request.args["choix"] != "":
        conn_db = get_db()
        ensemble_trouve = conn_db.liste_contravention_etablissement(
            request.args["choix"])

        return jsonify(ensemble_trouve)

    else:
        titre = "Erreur Système - 400"
        erreur_400 = True
        return render_template('erreur_400.html', titre=titre,
                               erreur_400=erreur_400), 400


# Cette fonction était pour la tache C1
@app.route('/api/nombre_amende_etablissement/json', methods=["GET"])
def recherche_contrevenants_json():
    conn_db = get_db()
    ensemble_trouve = conn_db.nombre_contravention()

    return jsonify(ensemble_trouve)


# Cette fonction était pour la tache C2
@app.route('/api/nombre_amende_etablissement/xml', methods=["GET"])
def recherche_contrevenants_xml():
    conn_db = get_db()
    ensemble_trouve = conn_db.nombre_contravention()
    xml_information = construction_xml(ensemble_trouve)

    return Response(xml_information, mimetype='text/xml')


# Cette fonction était pour la tache C3
@app.route('/api/nombre_amende_etablissement/csv', methods=["GET"])
def recherche_contrevenants_csv():
    conn_db = get_db()
    ensemble_trouve = conn_db.nombre_contravention()
    csv_information = construction_csv(ensemble_trouve)

    return Response(csv_information, mimetype='text/csv')


# Cette fonction est pour la tache D1
@app.route('/api/nouvelle_plainte', methods=["GET", "POST"])
@schema.validate(nouvelle_plainte_etablissement)
def creation_plainte():
    if request.method == "POST":
        liste_champs_plainte = initial_champ_nouvelle_plainte()
        liste_champs_plainte = remplissage_champ_nouvelle_plainte(
            request, liste_champs_plainte)
        conn_db = get_db()
        liste_champs_plainte['id_plainte'] = conn_db.inserer_nouvelle_plainte(
            liste_champs_plainte['etablissement'],
            liste_champs_plainte['no_civique'],
            liste_champs_plainte['nom_rue'],
            liste_champs_plainte['ville'],
            liste_champs_plainte['date_visite'],
            liste_champs_plainte['prenom_plaignant'],
            liste_champs_plainte['nom_plaignant'],
            liste_champs_plainte['description'])

        return jsonify({"Voici le numéro de la plainte ouverte":
                        liste_champs_plainte['id_plainte']}), 201

    elif request.method == "GET":
        titre = "Nouvelle plainte"
        return render_template("formulaire_plainte.html", titre=titre)


# Cette fonction est pour la tache D2
@app.route('/api/plainte/<id_plainte>', methods=["DELETE"])
def suppression_plainte(id_plainte):
    conn_db = get_db()
    no_plainte = conn_db.verification_existance_plainte(id_plainte)

    if no_plainte is None:
        return "", 404
    else:
        conn_db.suppression_plainte_existante(no_plainte)
        return {"La plainte a bien été supprimée": no_plainte}, 200


# Cette fonction est pour la tache E1
@app.route('/api/nouveau_profil', methods=["GET", "POST"])
@schema.validate(nouveau_profil)
def creation_profil():
    if request.method == "POST":
        liste_champs_profil = initial_champ_nouveau_profil()
        liste_champs_profil = remplissage_champ_nouvelle_profil(
            request, liste_champs_profil)
        conn_db = get_db()
        conn_db.inserer_nouveau_profil(
            liste_champs_profil['nom'], liste_champs_profil['prenom'],
            liste_champs_profil['courriel'], liste_champs_profil['password'],
            liste_champs_profil['salt'],
            liste_champs_profil['liste_etablissement'])

        return jsonify({"Création du nouveau profil": "Succès !"}), 201


def main():
    importation_donnees()


# Cette fonction était pour la tache A1
if __name__ == "__main__":
    main()
