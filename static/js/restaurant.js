// Variable pour la recherche par interval de date
const form_interval = document.querySelector('#recherche_par_interval');
const champ_date_debut = document.querySelector('#date_debut');
const champ_date_fin = document.querySelector('#date_fin');
const btn_reset_interval = document.querySelector('#btn_reset_interval');
const message_erreur_interval = document.querySelector('#message_erreur_interval');
const result_interval = document.querySelector('#result_interval');
const result_interval_etablissement = document.querySelector('#result_interval_etablissement');

// Variable pour la recherche par établissement précis après avoir sélectionner
const partie_cache = document.querySelector('.partie_cache');
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
    $(btn_reset_interval).click(function() {
        champ_date_debut.defaultValue = "";
        champ_date_fin.defaultValue = "";
        result_interval.innerHTML = "";
        effacer_messages_erreurs(message_erreur_interval);
        initialiser_tous_champs("input[type=text]");
        initialiser_tous_champs("#recherche_par_interval");
        initialiser_tous_champs(".partie_cache");
    });
}

function initialiser_tous_champs(type_champs){
    var tous_champs = document.querySelectorAll(type_champs);
    tous_champs.forEach(function(un_champ){
        if (type_champs == "input[type=text]"){
            un_champ.style.background = "white";
            un_champ.style.border = "1px solid #ccc";
        } else if (type_champs == "#recherche_par_interval"){
            un_champ.style.border = "2px solid black";
        } else if (type_champs == ".partie_cache"){
            partie_cache.style.display = "none";
            destruction_des_options();
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

// Les deux requêtes ajax passeront par la même entrée mais devront être différenciées
// On va utiliser la vérification de l'attribut «display» de la section cachée
function recherche_par_interval(){
    $(form_interval).submit(function (e) {
        e.preventDefault();
        var erreur_general = false;
        var erreur_localise = false;
        var pattern_date = new RegExp("^([0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])$");
        message_erreur_interval.innerHTML = ""; // On remet la section des messages vide
        erreur_general = verification_date_debut (pattern_date, erreur_localise, erreur_general);
        erreur_general = verification_date_fin (pattern_date, erreur_localise, erreur_general);
        if (partie_cache.style.display == "flex"){
            erreur_general = verification_choix_etablissement(erreur_localise, erreur_general);
            appel_ajax_interval_etablissement(erreur_general);
        } else {
            appel_ajax_interval(erreur_general);
        }
    });
}

function verification_date_debut(pattern_date, erreur_localise, erreur_general){
    if (champ_date_debut.value == "") {
        message_erreur_interval.innerHTML += "<li>Le champ «Date début» ne peut être vide !</li>";
        erreur_localise = true;
    } else if (!(pattern_date.test(champ_date_debut.value))) {
        message_erreur_interval.innerHTML += "<li>Le champ «Date début» ne contient pas une date au format ISO 8601 !</li>";
        erreur_localise = true;
    }

    if (erreur_localise){
        champ_date_debut.style.border = "2px solid red";
        champ_date_debut.style.background = "#FCDEDE";
        erreur_general = true;
    } else {
        champ_date_debut.style.background = "white";
        champ_date_debut.style.border = "1px solid #ccc";
    }

    return erreur_general;
}

function verification_date_fin(pattern_date, erreur_localise, erreur_general){
    if (champ_date_fin.value == "") {
        message_erreur_interval.innerHTML += "<li>Le champ «Date fin» ne peut être vide !</li>";
        erreur_localise = true;
    } else if (!(pattern_date.test(champ_date_fin.value))) {
        message_erreur_interval.innerHTML += "<li>Le champ «Date fin» ne contient pas une date au format ISO 8601 !</li>";
        erreur_localise = true;
    }

    if (erreur_localise){
        champ_date_fin.style.border = "2px solid red";
        champ_date_fin.style.background = "#FCDEDE";
        erreur_general = true;
    } else {
        champ_date_fin.style.background = "white";
        champ_date_fin.style.border = "1px solid #ccc";
    }

    return erreur_general;
}

function verification_choix_etablissement(erreur_localise, erreur_general){
    if (champ_etablissement.value == "") {
        message_erreur_interval.innerHTML += "<li>Vous devez sélectionner un établissement parmis la liste !</li>";
        erreur_localise = true;
    }

    if (erreur_localise){
        champ_etablissement.style.border = "2px solid red";
        champ_etablissement.style.background = "#FCDEDE";
        erreur_general = true;
    } else {
        champ_etablissement.style.background = "white";
        champ_etablissement.style.border = "1px solid #ccc";
    }

    return erreur_general;
}

function appel_ajax_interval(erreur_general){
    destruction_des_options(); // On retire toutes les options avant d'insérer les nouvelles
    if (!erreur_general){
        var ajax = new XMLHttpRequest();
        ajax.onreadystatechange = function() {
            if (ajax.readyState === XMLHttpRequest.DONE) {
                if (ajax.status === 200) {
                    var liste = JSON.parse(ajax.responseText);
                    if (liste.length > 0){
                        var ensemble_result = creation_bloc_html_interval(liste);
                        result_interval.innerHTML = ensemble_result['result_interval'];
                        construction_des_options(ensemble_result['result_etablissement'])
                        partie_cache.style.display = "flex";
                        form_interval.style.border = "2px solid black";
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
        ajax.open("POST", "/api/contrevenants/"+param, true);
        ajax.send();
    } else {
        form_interval.style.border = "2px solid red";
    }
}

function appel_ajax_interval_etablissement(erreur_general){
    if (!erreur_general){
        var ajax = new XMLHttpRequest();
        ajax.onreadystatechange = function() {

        };
        var param = `du=${champ_date_debut.value}&au=${champ_date_fin.value}&etablissement=${champ_etablissement.value}`;
        ajax.open("GET", "/api/contrevenant/"+param, true);
        ajax.send();



    } else {
        form_interval.style.border = "2px solid red";
    }
}


// Cette fonction sera utilisée pour caché la section du menu déroulant si le résultat retourne rien
// Les anciennes information du tableau des établissements avec leur nombre de contravention n'est plus valide
function appel_ajax_interval_succes_mais_erreur(){
    partie_cache.style.display = "none";
    result_interval.innerHTML = "";
    form_interval.style.border = "2px solid red";
}

function construction_des_options(liste_options){
    for(var i = 0; i < liste_options.length; i++) {
        var une_option = new Option(liste_options[i], liste_options[i]);
        $(une_option).html(liste_options[i]);
        $(champ_etablissement).append(une_option);
    }
}

function destruction_des_options(){
    $(champ_etablissement)
    .find('option')
    .remove()
    .end()
    .append('<option selected value="">À Sélectionner</option>')
    .val('');
}

// J'ai découvert comment faire des string avec des variables
// https://stackoverflow.com/questions/19105009/how-to-insert-variables-in-javascript-strings/44510325
function creation_bloc_html_interval(liste){
    // La liste des établissements à insérer plutard comme option du menu déroulant
    var result_etablissement = [];
    // Le bloc HTML pour le résultat de la liste des établissements ave leur nombre de contrevantions
    var result_interval = "<p>Voici le résultat des établissements avec leur nombre respectif de contrevention</p>";
    result_interval += "<table class=\"tabeau_resto\">";
    result_interval += "<thead><tr><th class=\"nom\">Établissement</th>";
    result_interval += "<th class=\"quantite\">Nombre</th></tr></thead><tbody>";
    for(var i = 0; i < liste.length; i++) {
        result_interval += "<tr>";
        var resto = liste[i];
        result_etablissement.push(resto.etablissement);
        result_interval += `<td class='nom'>${resto.etablissement}</td>`;
        result_interval += `<td class='quantite'>${resto.nombre}</td>`;
        result_interval += "<tr>";
    }
    result_interval += "</tbody></table>";

    return {'result_interval': result_interval, 'result_etablissement': result_etablissement};
}

document.addEventListener('DOMContentLoaded', function () {
    validation_champs_recherches();
    recherche_par_interval();
    reset_recherche();
    reset_recherche_interval();
});