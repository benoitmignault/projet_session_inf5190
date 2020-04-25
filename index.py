from functools import wraps

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.combining import OrTrigger
from apscheduler.triggers.cron import CronTrigger
from flask import Flask, Response, jsonify, redirect, make_response
from flask import render_template, request, session, url_for, abort
from flask_json_schema import JsonSchema
from flask_json_schema import JsonValidationError

from json_schema.gestion_etablissement_profil import \
    ajouter_plusieurs_etablissement, supprimer_etablissement
from modules.fonction import *
from json_schema.validateur_plainte import nouvelle_plainte_etablissement
from json_schema.validateur_profil import nouveau_profil

app = Flask(__name__, static_url_path='', static_folder='static')
schema = JsonSchema(app)
# Déclaration de la secret key pour me permettre utiliser
# les variables de sessions
app.secret_key = "(*&*&322387he738220)(*(*22347657"


@app.errorhandler(404)
def not_found_404(e):
    erreur_404 = True
    titre = "Page inexistante"
    return render_template("erreur_404.html", titre=titre,
                           erreur_404=erreur_404), 404


@app.errorhandler(400)
def not_found_400(e):
    titre = "Erreur Système - 400"
    erreur_400 = True
    return render_template('erreur_400.html', titre=titre,
                           erreur_400=erreur_400), 400


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


# Cette fonction est pour la route A2
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


# Cette fonction est pour la route A2 pour afficher le résultat
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


# Cette fonction est pour la route A3 et pour B1, B2, E3
def mise_jour_contrevenants():
    scheduler = BackgroundScheduler(daemon=True)
    trigger = OrTrigger([CronTrigger(day_of_week='*', hour=0, minute=0)])
    scheduler.start()
    scheduler.add_job(mise_jour_bd, trigger)


# Cette fonction est pour la route A4 et A5
@app.route('/api/liste_des_contrevenants/interval', methods=["GET", "POST"])
def recherche_contrevenants_interval():
    conn_db = get_db()
    liste_champs_interval = initial_champ_interval()
    liste_validation_interval = initial_champ_interval_validation()
    liste_champs_interval = remplissage_champs_interval(
        liste_champs_interval, request.args["du"], request.args["au"])
    liste_validation_interval = validation_champs_interval(
        liste_champs_interval, liste_validation_interval)
    liste_validation_interval = situation_erreur_interval(
        liste_validation_interval)
    if not liste_validation_interval['situation_erreur']:
        if request.method == "GET":
            ensemble_trouve = conn_db.liste_contravention_interval(
                liste_champs_interval['date_debut'],
                liste_champs_interval['date_fin'])

            return jsonify(ensemble_trouve)

        else:
            ensemble_trouve = conn_db.nombre_contravention_interval(
                liste_champs_interval['date_debut'],
                liste_champs_interval['date_fin'])
            return jsonify(ensemble_trouve)

    else:
        return abort(400)


# Cette fonction était pour la tache A6
@app.route('/api/liste_des_contrevenants/etablissement', methods=["GET"])
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
@app.route('/api/liste_des_contrevenants/json', methods=["GET"])
def recherche_contrevenants_json():
    conn_db = get_db()
    ensemble_trouve = conn_db.nombre_contravention()

    return jsonify(ensemble_trouve)


# Cette fonction était pour la tache C2
@app.route('/api/liste_des_contrevenants/xml', methods=["GET"])
def recherche_contrevenants_xml():
    conn_db = get_db()
    ensemble_trouve = conn_db.nombre_contravention()
    xml_information = construction_xml(ensemble_trouve)

    return Response(xml_information, mimetype='text/xml')


# Cette fonction était pour la tache C3
@app.route('/api/liste_des_contrevenants/csv', methods=["GET"])
def recherche_contrevenants_csv():
    conn_db = get_db()
    ensemble_trouve = conn_db.nombre_contravention()
    csv_information = construction_csv(ensemble_trouve)

    return Response(csv_information, mimetype='text/csv')


# Cette fonction est pour la tache D1 du service REST
@app.route('/api/nouvelle_plainte', methods=["POST"])
@schema.validate(nouvelle_plainte_etablissement)
def api_creation_plainte():
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


# Cette fonction est pour la tache D1 de l'interface web
@app.route('/nouvelle_plainte', methods=["GET"])
def creation_plainte():
    titre = "Nouvelle plainte"
    conn_db = get_db()
    liste_etablissement = conn_db.liste_tous_restaurants()
    return render_template("formulaire_plainte.html", titre=titre,
                           liste_etablissement=liste_etablissement)


# Cette fonction est pour la tache D2
@app.route('/api/plainte/<id_plainte>', methods=["DELETE"])
def suppression_plainte(id_plainte):
    conn_db = get_db()
    no_plainte = conn_db.verification_existance_plainte(id_plainte)

    if no_plainte is None:
        return abort(404)
    else:
        conn_db.suppression_plainte_existante(no_plainte)
        return {"La plainte a bien été supprimée": no_plainte}, 200


# Cette fonction est pour la tache E1
@app.route('/api/nouveau_profil', methods=["POST"])
@schema.validate(nouveau_profil)
def api_creation_profil():
    conn_db = get_db()
    liste_champs_profil = initial_champ_nouveau_profil()
    liste_champs_profil = remplissage_champ_nouveau_profil(
        request, liste_champs_profil)

    courriel = conn_db.verification_profil_existant(
        liste_champs_profil['courriel'])

    if courriel is None:
        conn_db.inserer_nouveau_profil(
            liste_champs_profil['nom'], liste_champs_profil['prenom'],
            liste_champs_profil['courriel'],
            liste_champs_profil['password_hasher'],
            liste_champs_profil['salt'],
            liste_champs_profil['liste_etablissement'])

        return jsonify({"Création du nouveau profil": "Succès !"}), 201

    else:
        return jsonify({"Impossible de créer le profil":
                            "Courriel est déjà présent !"}), 404


# Cette fonction est pour la tache E2
@app.route('/nouveau_profil', methods=["GET"])
def creation_profil():
    conn_db = get_db()

    liste_etablissement = conn_db.liste_tous_restaurants()
    titre = "Création d'un profil"
    return render_template('creation_profil.html', titre=titre,
                           liste_etablissement=liste_etablissement)


# Cette fonction est pour la tache E2
@app.route('/connection', methods=["GET", "POST"])
def connexion_profil():
    if request.method == "GET":
        titre = "Page de Connexion !"
        return render_template("connection.html", courriel="", password="",
                               titre=titre, messages=[], erreur=False)

    elif request.method == "POST":
        liste_champs_connexion = initial_champ_connexion()
        liste_validation_connexion = initial_champ_connexion_validation()
        liste_champs_connexion = remplissage_champ_connexion(
            request.form, liste_champs_connexion)
        conn_db = get_db()
        utilisateur = conn_db.recuperation_info_connexion(
            liste_champs_connexion['courriel'])
        if utilisateur is None:
            liste_validation_connexion['champ_courriel_non_trouve'] = True

        else:
            liste_champs_connexion = remplissage_post_verification_conn(
                liste_champs_connexion, utilisateur)

        liste_validation_connexion = validation_champ_connexion(
            liste_champs_connexion, liste_validation_connexion)
        liste_validation_connexion = situation_erreur_interval(
            liste_validation_connexion)

        if not liste_validation_connexion['situation_erreur']:
            id_session = uuid.uuid4().hex
            conn_db.creation_session_active(id_session,
                                            liste_champs_connexion['courriel'])
            session["id"] = id_session
            return redirect(url_for('.profil_connecter'))

        else:
            liste_champs_connexion['messages'] = message_erreur_connexion(
                liste_validation_connexion)
            titre = "Erreur de la Connexion !"

            return render_template("connection.html", titre=titre, erreur=True,
                                   messages=liste_champs_connexion['messages'],
                                   liste_validation=liste_validation_connexion,
                                   courriel=liste_champs_connexion['courriel'],
                                   password=liste_champs_connexion['password'])


def authentification_requise(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not is_authenticated(session):
            return personne_non_autorisee()
        return f(*args, **kwargs)

    return decorated


# Cette fonction est pour la tache E2 et l'authentification avec succès
@app.route('/connecter/profil', methods=["GET"])
@authentification_requise
def profil_connecter():
    conn_db = get_db()
    courriel = conn_db.recuperation_session_active(session["id"])
    if request.method == "GET":
        liste_infos = initial_infos_connecter()
        info_profil = conn_db.recuperation_profil(courriel)
        etablissement = conn_db.recuperation_profil_etablissement(
            info_profil[3])
        etablissement_dispo = conn_db.recuperation_etablissement_restant(
            info_profil[3])
        liste_infos = remplissage_infos_connecter(liste_infos, info_profil)

        titre = "Vous êtes maintenant connecté !"
        return render_template("utilisateur_connecter.html", titre=titre,
                               liste_infos=liste_infos,
                               etablissement=etablissement,
                               etablissement_dispo=etablissement_dispo)


# Cette fonction est pour la tache E2
@app.route('/connecter/gestion_photo', methods=["POST"])
@authentification_requise
def ajouter_photo():
    fichier_photo = None
    id_photo_nouvelle = None
    id_photo_ancienne = None
    id_personne = ""
    type_photo = ""

    if "photo" in request.files:
        fichier_photo = request.files["photo"]
        type_photo = request.files["photo"].content_type
        if type_photo == "image/png":
            type_photo = "png"

        else:
            type_photo = "jpg"

        id_photo_nouvelle = str(uuid.uuid4().hex)

    if "id_photo" in request.form:
        id_photo_ancienne = request.form["id_photo"]

    if "id_personne" in request.form:
        id_personne = request.form["id_personne"]

    if id_photo_nouvelle is not None:
        conn_db = get_db()

        if "ajout" in request.form:
            conn_db.ajouter_photo(id_photo_nouvelle, fichier_photo)
            conn_db.ajout_id_photo_profil(
                id_photo_nouvelle, id_personne, type_photo)

        elif "modifier" in request.form:
            conn_db.supprimer_photo_profil(id_photo_ancienne)
            conn_db.supprimer_lien_photo_profil(id_personne)
            conn_db.ajouter_photo(id_photo_nouvelle, fichier_photo)
            conn_db.ajout_id_photo_profil(
                id_photo_nouvelle, id_personne, type_photo)

        return redirect(url_for('.profil_connecter'))

    else:
        return abort(404)


# Cette fonction est pour la tache E2
@app.route('/api/connecter/supprimer_photo', methods=["DELETE"])
@authentification_requise
def supprimer_photo():
    conn_db = get_db()
    data = request.get_json()
    id_personne = data["id_personne"]
    id_photo = data["id_photo"]

    if id_personne == "" or id_photo == "":
        return abort(404)

    else:
        conn_db.supprimer_photo_profil(id_photo)
        conn_db.supprimer_lien_photo_profil(id_personne)

        return "", 200


# Cette fonction est pour la tache E2
@app.route('/image/<id_photo>.<type_photo>')
@authentification_requise
def faire_afficher_photo(id_photo, type_photo):
    conn_db = get_db()
    binary_data = conn_db.recuperer_photo(id_photo)
    if binary_data is None:
        return Response(status=404)
    else:
        response = make_response(binary_data)
        if type_photo == "png":
            response.headers.set('Content-Type', 'image/png')

        else:
            response.headers.set('Content-Type', 'image/jpeg')

    return response


# Cette fonction est pour la tache E2
@app.route('/api/connecter/ajouter_etablissement', methods=["POST"])
@schema.validate(ajouter_plusieurs_etablissement)
@authentification_requise
def ajouter_etablissement():
    conn_db = get_db()
    liste_champs_ajout = initial_champ_ajout_etablissement()
    liste_champs_ajout = remplissage_champ_ajout_etablissement(
        request, liste_champs_ajout)
    conn_db.inserer_etablissement_surveiller_profil(
        liste_champs_ajout['id_personne'],
        liste_champs_ajout['liste_etablissement'])

    etablissement = conn_db.recuperation_profil_etablissement(
        liste_champs_ajout['id_personne'])
    etablissement_dispo = conn_db.recuperation_etablissement_restant(
        liste_champs_ajout['id_personne'])
    return jsonify({"etablissement": etablissement,
                    "etablissement_dispo": etablissement_dispo}), 200


# Cette fonction est pour la tache E2
@app.route('/api/connecter/retirer_etablissement', methods=["DELETE"])
@schema.validate(supprimer_etablissement)
@authentification_requise
def retirer_etablissement():
    conn_db = get_db()
    data = request.get_json()
    id_surveillance = conn_db.verification_etablissement_surveiller(
        data['id_surveillance'])

    if id_surveillance is None:
        return abort(404)

    else:
        conn_db.supprimer_etablissement_profil(
            data['id_personne'], id_surveillance)
        etablissement_dispo = conn_db.recuperation_etablissement_restant(
            data['id_personne'])

        return jsonify(etablissement_dispo), 200


# Cette fonction est pour la tache E4
@app.route('/connecter/desabonnement/<lien>', methods=["GET"])
def desabonnement(lien):
    conn_db = get_db()
    info_desabonnement = conn_db.verif_lien_desabonnement(lien)
    if info_desabonnement is None:

        return abort(404)

    else:
        titre = "Page de désabonnement"

        return render_template("desabonnement_etablissement.html",
                               titre=titre, lien=lien,
                               etablissement=info_desabonnement[0])


# Cette fonction est pour la tache E4
@app.route('/api/connecter/desabonnement', methods=["DELETE"])
def desabonner():
    conn_db = get_db()
    data = request.get_json()
    info_desabonnement = conn_db.verif_lien_desabonnement(
        data['lien_desabonnement'])
    if info_desabonnement is None:
        return jsonify({
            "message_erreur":
                "<p>Attention ! Le lien pour se désabonner "
                "n'existe pas !</p>"}), 404

    else:
        conn_db.supprimer_abonnement_etablissement(
            data['lien_desabonnement'])
        return "", 200


# Cette fonction est pour la tache E2
@app.route('/deconnection')
@authentification_requise
def deconnection_profil():
    id_session = session["id"]
    session.pop('id', None)
    conn_db = get_db()
    conn_db.detruire_session_active(id_session)
    return redirect(url_for('.home'))


# Cette fonction est pour la tache E2
def is_authenticated(session):
    return "id" in session


# Cette fonction est pour la tache E2
def personne_non_autorisee():
    return Response("Vous tentez d''accéder à une page web sécurité !<br>"
                    "Veuillez vous authentifiez avec ce lien :<br> "
                    "<a href=\"/connection\">Se Connecter</a>'"
                    , 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})


# Cette fonction était pour la tache D3
@app.route('/liste_des_contrevenants/interval', methods=["GET"])
def liste_contravention_par_etablissement():
    liste_champs_precis = initial_champ_precis()
    liste_champs_precis_valid = initial_champ_precis_validation()
    liste_champs_precis = remplissage_champs_precis(
        liste_champs_precis, request.args)
    liste_champs_precis_valid = validation_champs_precis(
        liste_champs_precis, liste_champs_precis_valid)
    liste_champs_precis_valid = situation_erreur_interval(
        liste_champs_precis_valid)
    if not liste_champs_precis_valid['situation_erreur']:
        conn_db = get_db()
        ensemble_trouve = conn_db.recuperation_interval_precis(
            liste_champs_precis["date_debut"], liste_champs_precis["date_fin"],
            liste_champs_precis["etablissement"])
        ensemble_ajuster = conn_db.verification_ensemble_modifier(
            ensemble_trouve)
        nombre = len(ensemble_ajuster)
        titre = "Résultat - précis !"

        return render_template("recherche_precise_trouve.html", titre=titre,
                               ensemble_ajuster=ensemble_ajuster,
                               etablissement=
                               liste_champs_precis["etablissement"],
                               nombre=nombre)

    else:
        return abort(404)


# La fonction sera exécuté à chaque jour à minuit, automatiquement
mise_jour_contrevenants()

# Cette fonction était pour la tache A1
if __name__ == "__main__":
    importation_donnees()
