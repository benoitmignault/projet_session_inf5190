// Variable pour la recherche par interval de date
const form_interval = document.querySelector('#recherche_par_interval');
const champ_date_debut = document.querySelector('#date_debut');
const champ_date_fin = document.querySelector('#date_fin');
const btn_reset_interval = document.querySelector('#btn_reset_interval');
const message_erreur_interval = document.querySelector('#message_erreur_interval');
const result_interval = document.querySelector('#result_interval');
const result_interval_etablissement = document.querySelector('#result_interval_etablissement');

// Variable pour la recherche par établissement précis après avoir sélectionner
const champ_liste_resto = document.querySelector('#liste_resto');

// Variables pour la recherche d'information générale pour être utiliser avec le bouton effacer
const champ_nom_resto = document.querySelector('#etablissement');
const champ_nom_proprio = document.querySelector('#proprietaire');
const champ_nom_rue = document.querySelector('#nom_rue');
const btn_reset_recher = document.querySelector('#btn_reset_recher');
const message_erreur_recher = document.querySelector('#message_erreur_recher');

// Variable pour l'ajout d'une demande de plainte
const form_nouvelle_plainte = document.querySelector('#nouvelle_plainte');
const message_erreur_plainte = document.querySelector('#message_erreur_plainte');
const champ_etablissement = document.querySelector('#etablissement');
const champ_no_civique = document.querySelector('#no_civique');
const champ_nom_rue_plainte = document.querySelector('#nom_rue');
const champ_nom_ville = document.querySelector('#nom_ville');
const champ_code_postal = document.querySelector('#code_postal');
const champ_date_visite = document.querySelector('#date_visite');
const champ_prenom_plaignant = document.querySelector('#prenom_plaignant');
const champ_nom_plaignant = document.querySelector('#nom_plaignant');
const champ_description = document.querySelector('#description');

const pattern_date = new RegExp("^([0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])$");

function initial_champ_ajax_validation(){
    var liste_validation = {"champ_debut_inv": false, "aucun_choix": false,
                        "champ_fin_inv": false, "champ_debut_vide": false,
                        "champ_fin_vide": false, "champ_liste_resto_vide": false,
                        "les_deux_choix": false, "champs_date_vides": false};

    return liste_validation;
}

function reset_recherche(){
    $(btn_reset_recher).click(function() {
        champ_nom_resto.defaultValue = "";
        champ_nom_proprio.defaultValue = "";
        champ_nom_rue.defaultValue = "";
        effacer_messages_erreurs(message_erreur_recher);
        initialiser_tous_champs("input[type=text]");
        initialiser_tous_champs("#recherche");
    });
}

function reset_recherche_interval(){
    $(btn_reset_interval).click(function() {
        champ_date_debut.defaultValue = "";
        champ_date_fin.defaultValue = "";
        result_interval.innerHTML = "";
        result_interval_etablissement.innerHTML = "";
        effacer_messages_erreurs(message_erreur_interval);
        initialiser_tous_champs("input[type=text]");
        initialiser_tous_champs("#liste_resto");
        initialiser_tous_champs("#recherche_par_interval");
    });
}

function initialiser_tous_champs(type_champs){
    var tous_champs = document.querySelectorAll(type_champs);
    tous_champs.forEach(function(un_champ){
        if (type_champs == "input[type=text]" || type_champs == "#liste_resto"){
            un_champ.style.background = "white";
            un_champ.style.border = "1px solid #ccc";
        } else if (type_champs == "#recherche_par_interval" || type_champs == "#recherche"){
            un_champ.style.border = "2px solid black";
        }
    });
}

function effacer_messages_erreurs(message){
    // Nous devons vérifier que les variables ne sont pas égales à «undefined»
    if (message){
        message.innerHTML = "";
    }
}

function validation_champs_recherches(){
    var regex_resto = "^[a-z1-9A-Z][a-z0-9- 'A-Z@_!#$%^&*()<>?/\\|}{~:]{3,98}[a-z0-9A-Z.)]$";
    var regex_proprio = "^[a-z1-9A-Z][a-z0-9- 'A-Z@_!#$%^&*()<>?/\\|}{~:]{3,63}[a-z0-9A-Z.)]$";
    var regex_rue = "^[a-z1-9A-Z][a-z0-9- 'A-Z]{1,33}[a-z0-9A-Z]$"

    $(champ_nom_resto).change(function () {
        validation_regex(champ_nom_resto, regex_resto);
    });

    $(champ_nom_proprio).change(function () {
        validation_regex(champ_nom_proprio, regex_proprio);
    });

    $(champ_nom_rue).change(function () {
        validation_regex(champ_nom_rue, regex_rue);
    });
}

function validation_regex(champ, type_regex){
    var re = new RegExp(type_regex);
    if (!(re.test(champ.value))) {
        alert("Veuillez respecter les charactères permis et la longueur permise !");
        champ.value = "";
    }
}

function recherche_rapide(){
    $(form_interval).submit(function (e) {
        e.preventDefault();
        message_erreur_interval.innerHTML = ""; // On remet la section des messages vide
        var liste_validation = initial_champ_ajax_validation();
        liste_validation = verification_interval(liste_validation);
        liste_validation = verification_choix_etablissement(liste_validation);
        message_erreur_ajax(liste_validation);
        ajustement_style_champs(liste_validation);
        if (!liste_validation['champs_date_vides'] && liste_validation['champ_liste_resto_vide']){
            result_interval.innerHTML = "";
            result_interval_etablissement.innerHTML = "";
            if (!liste_validation['champ_debut_inv'] && !liste_validation['champ_fin_inv'] &&
                !liste_validation['champ_debut_vide'] && !liste_validation['champ_fin_vide']){
                appel_ajax_interval();
            }

        } else if (liste_validation['champs_date_vides'] && !liste_validation['champ_liste_resto_vide']) {
            result_interval.innerHTML = "";
            result_interval_etablissement.innerHTML = "";
            appel_ajax_interval_etablissement();
        // Si non, nous avons eu une erreur et on efface les vieux résultats pour éviter de la confusion
        } else {
            result_interval.innerHTML = "";
            result_interval_etablissement.innerHTML = "";
        }
    });
}

function demande_plainte(){
    $(form_nouvelle_plainte).submit(function (e) {
        e.preventDefault();
        message_erreur_plainte.innerHTML = ""; // On remet la section des messages vide
        appel_ajax_nouvelle_plainte();

    });

}
function verification_interval(liste_validation){
    if (champ_date_debut.value == "") {
        liste_validation['champ_debut_vide'] = true;
    } else if (!(pattern_date.test(champ_date_debut.value))) {
        liste_validation['champ_debut_inv'] = true;
    }

    if (champ_date_fin.value == "") {
        liste_validation['champ_fin_vide'] = true;
    } else if (!(pattern_date.test(champ_date_fin.value))) {
        liste_validation['champ_fin_inv'] = true;
    }

    if (liste_validation['champ_debut_vide'] && liste_validation['champ_fin_vide']){
        liste_validation['champs_date_vides'] = true;
    }

    return liste_validation;
}

function verification_choix_etablissement(liste_validation){
    if (champ_liste_resto.value == "") {
        liste_validation['champ_liste_resto_vide'] = true;
    }

    if ( (!liste_validation['champ_debut_vide'] || !liste_validation['champ_fin_vide']) && !liste_validation['champ_liste_resto_vide']){
        liste_validation['les_deux_choix'] = true;
    }

    if (liste_validation['champs_date_vides'] && liste_validation['champ_liste_resto_vide']){
        liste_validation['aucun_choix'] = true;
    }

    return liste_validation;
}

function message_erreur_ajax(liste_validation){
    if (liste_validation['aucun_choix'] || liste_validation['les_deux_choix']){
        if (liste_validation['aucun_choix']){
            message_erreur_interval.innerHTML += "<li>Veuiller choisir au moins une des deux options !</li>";
        } else if (liste_validation['les_deux_choix']){
            message_erreur_interval.innerHTML += "<li>Veuiller choisir une seul des deux options !</li>";
        }
    } else {
        if (liste_validation['champ_debut_inv']){
            message_erreur_interval.innerHTML += "<li>Le champ «Date début» ne contient pas une date au format ISO 8601 !</li>";
        }

        if (liste_validation['champ_fin_inv']){
            message_erreur_interval.innerHTML += "<li>Le champ «Date fin» ne contient pas une date au format ISO 8601 !</li>";
        }

        if (liste_validation['champ_liste_resto_vide'] && liste_validation['champ_debut_vide'] && !liste_validation['champ_fin_vide']){
            message_erreur_interval.innerHTML += "<li>Le champ «Date début» ne peut être vide !</li>";
        }

        if (liste_validation['champ_liste_resto_vide'] && !liste_validation['champ_debut_vide'] && liste_validation['champ_fin_vide']){
            message_erreur_interval.innerHTML += "<li>Le champ «Date fin» ne peut être vide !</li>";
        }
    }
}

function ajustement_style_champs(liste_validation){
    if (liste_validation['champ_debut_inv'] || (liste_validation['champ_debut_vide'] && liste_validation['champ_liste_resto_vide'])){
        modification_erreur(champ_date_debut);
    } else {
        modification_correct(champ_date_debut);
    }

    if (liste_validation['champ_fin_inv'] || (liste_validation['champ_fin_vide'] && liste_validation['champ_liste_resto_vide'])){
        modification_erreur(champ_date_fin);
    } else {
        modification_correct(champ_date_fin);
    }

    if (liste_validation['champ_liste_resto_vide'] && (liste_validation['aucun_choix'] || liste_validation['les_deux_choix'])){
        modification_erreur(champ_liste_resto);
    } else {
        modification_correct(champ_liste_resto);
    }

    if (liste_validation['aucun_choix'] || liste_validation['les_deux_choix']){
        modification_erreur(champ_date_debut);
        modification_erreur(champ_date_fin);
        modification_erreur(champ_liste_resto);
        form_interval.style.border = "2px solid red";
    } else {
        form_interval.style.border = "2px solid black";
    }
}

function modification_erreur(champ){
    champ.style.border = "2px solid red";
    champ.style.background = "#FCDEDE";
}

function modification_correct(champ){
    champ.style.border = "1px solid #ccc";
    champ.style.background = "white";
}

function appel_ajax_interval(){
    var ajax = new XMLHttpRequest();
    ajax.onreadystatechange = function() {
        if (ajax.readyState === XMLHttpRequest.DONE) {
            if (ajax.status === 200) {
                var liste = JSON.parse(ajax.responseText);
                if (liste.length > 0){
                    var resultat = creation_bloc_html_interval(liste);
                    result_interval.innerHTML = resultat;
                } else {
                    appel_ajax_interval_succes_mais_erreur();
                    message_erreur_interval.innerHTML += "<li>L'interval de date ne contenait aucune donnée !</li>";
                }
            } else {
                appel_ajax_interval_succes_mais_erreur();
                message_erreur_interval.innerHTML += "<li>Attention ! Il y a eu une erreur avec la réponse du serveur !</li>";
            }
        }
    };
    var param = `du=${champ_date_debut.value}&au=${champ_date_fin.value}`;
    ajax.open("GET", "/api/nombre_amende_etablissement/"+param, true);
    ajax.send();
}

function appel_ajax_interval_etablissement(){
    var ajax = new XMLHttpRequest();
    ajax.onreadystatechange = function() {
        if (ajax.readyState === XMLHttpRequest.DONE) {
            if (ajax.status === 200) {
                var liste = JSON.parse(ajax.responseText);
                result_interval_etablissement.innerHTML = creation_bloc_html_etablissement(liste);
            } else {
                appel_ajax_interval_succes_mais_erreur();
                message_erreur_interval.innerHTML += "<li>Attention ! Il y a eu une erreur avec la réponse du serveur !</li>";
            }
        }
    };
    var param = `etablissement=${champ_liste_resto.value}`;
    ajax.open("GET", "/api/liste_amendes_etablissement/"+param, true);
    ajax.send();
}

function appel_ajax_nouvelle_plainte(){
    console.log("je suis dans la fct ajax");
    var ajax = new XMLHttpRequest();
    var data = {
            "etablissement": "AILE BUFFALO BILL",
            "no_civique": 4084,
            "nom_rue": "Rue Saint-Denis",
            "ville": "Montréal H2W 2M5",
            "date_visite": "2018-05-28",
            "prenom_plaignant": "Benoît",
            "nom_plaignant": "Mignault",
            "description": "Nous avons remarqué la présence de petits animaux dans la cuisine"
        };
    var data_json = JSON.stringify(data);
    console.log(data_json);
    ajax.open("POST", "/api/nouvelle_plainte", true);
    ajax.setRequestHeader("Content-Type", "application/json");
    ajax.send(data_json);
}


function appel_ajax_interval_succes_mais_erreur(){
    result_interval.innerHTML = "";
    result_interval_etablissement.innerHTML = "";
    form_interval.style.border = "2px solid red";
}

// J'ai découvert comment faire des string avec des variables
// https://stackoverflow.com/questions/19105009/how-to-insert-variables-in-javascript-strings/44510325
function creation_bloc_html_interval(liste){
    // Le bloc HTML pour le résultat de la liste des établissements ave leur nombre de contrevantions
    var result_interval = "<table class=\"tabeau_resto\">";
    result_interval += "<thead><tr><th class=\"nom\">Établissement</th>";
    result_interval += "<th class=\"quantite\">Nombre</th></tr></thead><tbody>";
    for(var i = 0; i < liste.length; i++) {
        result_interval += "<tr>";
        var resto = liste[i];
        result_interval += `<td class='nom'>${resto.etablissement}</td>`;
        result_interval += `<td class='quantite'>${resto.nombre}</td>`;
        result_interval += "<tr>";
    }
    result_interval += "</tbody></table>";

    return result_interval;
}

// Utilisation de ce principe pour itérer
// https://zellwk.com/blog/looping-through-js-objects/
function creation_bloc_html_etablissement(liste){
    var result_liste = "";
    for(var i = 0; i < liste.length; i++) {
        result_liste += "<table class=\"tabeau_resto\"><tbody>";
        const une_amande = Object.entries(liste[i]);
        for (const [cle, valeur] of une_amande) {
            result_liste += "<tr>";
            result_liste += `<td class='cle'>${cle} :</td>`;
            if (cle == "Montant de l'amende"){
                result_liste += `<td class='valeur'>${valeur} $</td>`;
            } else {
                result_liste += `<td class='valeur'>${valeur}</td>`;
            }
            result_liste += "<tr>";
        }
        result_liste += "</tbody></table>";
    }

    return result_liste;
}

document.addEventListener('DOMContentLoaded', function () {
    validation_champs_recherches();
    recherche_rapide();
    demande_plainte();
    reset_recherche();
    reset_recherche_interval();
});