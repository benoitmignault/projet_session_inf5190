// Variable pour la recherche par interval de date
const form_interval = document.querySelector('#recherche_par_interval');
const champ_date_debut = document.querySelector('#date_debut');
const champ_date_fin = document.querySelector('#date_fin');
const btn_reset_interval = document.querySelector('#btn_reset_interval');
const message_erreur_interval = document.querySelector('#message_erreur_interval');
const result_interval = document.querySelector('#result_interval');
const result_interval_etablissement = document.querySelector('#result_interval_etablissement');

// Variable pour la recherche par établissement précit après avoir sélectionner
const champ_etablissement = document.querySelector('#liste_resto');

// Variables pour la recherche d'information générale pour être utiliser avec le bouton effacer
const champ_nom_resto = document.querySelector('#etablissement');
const champ_nom_proprio = document.querySelector('#proprietaire');
const champ_nom_rue = document.querySelector('#nom_rue');
const btn_reset_recher = document.querySelector('#btn_reset_recher');
const message_erreur_recher = document.querySelector('#message_erreur_recher');

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
    champ_date_debut.defaultValue = "";
    champ_date_fin.defaultValue = "";
    section_result.innerHTML = "";

    effacer_messages_erreurs(message_aucun_rapide);
    re_initialiser_tous_champs("input[type=text]");
}

function initialiser_tous_champs(type_champs){
    var tous_champs = document.querySelectorAll(type_champs);
    tous_champs.forEach(function(un_champ){
        if (type_champs == "input[type=text]"){
            un_champ.style.background = "white";
            un_champ.style.border = "1px solid #ccc";
        } else {
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

function recherche_rapide_par_interval(){
    $(form_interval).submit(function (e) {
        e.preventDefault();
        var erreur_general = false;
        var erreur_localise = false;
        var pattern_date = new RegExp("^([0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])$");
        message_aucun_rapide.innerHTML = ""; // On remet la section des messages vide
        erreur_general = verification_date_debut (pattern_date, erreur_localise, erreur_general);
        erreur_general = verification_date_fin (pattern_date, erreur_localise, erreur_general);
        appel_ajax(erreur_general);
    });
}

function verification_date_debut(pattern_date, erreur_localise, erreur_general){
    if (date_debut.value == "") {
        message_aucun_rapide.innerHTML += "<li>Le champ «Date début» ne peut être vide !</li>";
        erreur_localise = true;
    } else if (!(pattern_date.test(date_debut.value))) {
        message_aucun_rapide.innerHTML += "<li>Le champ «Date début» ne contient pas une date au format ISO 8601 valide !</li>";
        erreur_localise = true;
    }

    if (erreur_localise){
        date_debut.style.border = "2px solid red";
        date_debut.style.background = "#FCDEDE";
        erreur_localise = false; // on reset l'indicateur pour le prochain champ
        erreur_general = true;
    } else {
        date_debut.style.background = "white";
        date_debut.style.border = "1px solid #ccc";
    }

    return erreur_general;
}

function verification_date_fin(pattern_date, erreur_localise, erreur_general){
    if (date_fin.value == "") {
        message_aucun_rapide.innerHTML += "<li>Le champ «Date fin» ne peut être vide !</li>";
        erreur_localise = true;
    } else if (!(pattern_date.test(date_fin.value))) {
        message_aucun_rapide.innerHTML += "<li>Le champ «Date fin» ne contient pas une date au format ISO 8601 valide !</li>";
        erreur_localise = true;
    }

    if (erreur_localise){
        date_fin.style.border = "2px solid red";
        date_fin.style.background = "#FCDEDE";
        erreur_localise = false; // on reset l'indicateur pour le prochain champ
        erreur_general = true;
    } else {
        date_fin.style.background = "white";
        date_fin.style.border = "1px solid #ccc";
    }

    return erreur_general;
}

function appel_ajax(erreur_general){
    // On fait l'appel AJAX seulement si l'indication général est à false.
    if (!erreur_general){
        var ajax = new XMLHttpRequest();
        ajax.onreadystatechange = function() {
            if (ajax.readyState === XMLHttpRequest.DONE) {
                if (ajax.status === 200) {
                    section_result.innerHTML = creation_bloc_html(ajax);
                } else {
                    section_result.innerHTML = "Attention ! Il y a eu une erreur avec la réponse du serveur !";
                }
            }
        };
        var param = "du="+date_debut.value+"&au="+date_fin.value;
        ajax.open("POST", "/api/contrevenants/"+param, true);
        ajax.send();
    }
}

function creation_bloc_html(ajax){
    var liste = JSON.parse(ajax.responseText);
    var bloc_html = "<p>Voici le résultat des établissements avec leur nombre respectif de contrevention</p>";
    bloc_html += "<table class=\"tabeau_resto\">";
    bloc_html += "<thead><tr><th class=\"nom\">Établissement</th>";
    bloc_html += "<th class=\"quantite\">Nombre</th></tr></thead><tbody>";
    for(var i = 0; i < liste.length; i++) {
        bloc_html += "<tr>";
        var resto = liste[i];
        bloc_html += "<td class=\"nom\">" + resto.etablissement + "</td>";
        bloc_html += "<td class=\"quantite\">" + resto.nombre + "</td>";
        bloc_html += "<tr>";
    }
    bloc_html += "</tbody></table>";

    return bloc_html;
}

document.addEventListener('DOMContentLoaded', function () {
    validation_champs_recherches();
    recherche_rapide_par_interval();
    reset_recherche();
    reset_recherche_interval();
});