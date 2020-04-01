// Variable pour le bouton Effacer dans la page de recherche
const recher_nom_resto = document.querySelector('#etablissement');
const recher_nom_proprio = document.querySelector('#proprietaire');
const recher_nom_rue = document.querySelector('#nom_rue');

// Variable du formulaire qu'on voudra envoyer via appel AJAX
const formulaire = document.querySelector('#recherche_rapide');
const date_debut = document.querySelector('#date_debut');
const date_fin = document.querySelector('#date_fin');
const message_aucun_rapide = document.querySelector('#aucun_recherche_rapide');

// Variable pour effacer les messages
const message_aucun = document.querySelector('#aucun_recherche');

/*
    En fonction où nous sommes, sur le site, la fonction «re_initialiser_tous_champs» sera
    appelée pour chaque type de champs que le formulaire contient.
*/
function reset_recherche(){
    recher_nom_resto.defaultValue = "";
    recher_nom_proprio.defaultValue = "";
    recher_nom_rue.defaultValue = "";
    effacer_messages_erreurs(message_aucun);
    re_initialiser_tous_champs("input[type=text]");
    re_initialiser_tous_champs("#recherche");
}

function reset_recherche_rapide(){
    date_debut.defaultValue = "";
    date_fin.defaultValue = "";
    effacer_messages_erreurs(message_aucun_rapide);
    re_initialiser_tous_champs("input[type=text]");
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

    $(recher_nom_resto).change(function () {
        validation_regex(recher_nom_resto, regex_resto);
    });

    $(recher_nom_proprio).change(function () {
        validation_regex(recher_nom_proprio, regex_proprio);
    });

    $(recher_nom_rue).change(function () {
        validation_regex(recher_nom_rue, regex_rue);
    });
}

function validation_regex(champ, type_regex){
    var re = new RegExp(type_regex);
    if (!(re.test(champ.value))) {
        alert("Veuillez respecter les charactères permis et la longueur permise !");
        champ.value = "";
    }
}

/*
    Cette fonction aura pour but de remettre au valeur initial la bordure et couleur de fond
    sur tous les champs d'un formulaire
*/
function re_initialiser_tous_champs(type_champs){
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

function recherche_rapide_par_interval(){
    $(formulaire).submit(function (e) {
        var erreur_general = false; // Servira à vérifier si on a eu une erreur en cours de route
        var erreur_localise = false; // Servira à vérifier si on a eu une erreur en cours de route
        e.preventDefault();
        var pattern_date = new RegExp("^([0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])$");
        message_aucun_rapide.innerHTML = ""; // On remet la section des messages vide
        // Section pour la gestion du champ «date_debut»
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
            // Si nous avons saisi de quoi de valide
            date_debut.style.background = "white";
            date_debut.style.border = "1px solid #ccc";
        }
        // Fin de la section du champ «date_debut»
        // Section pour la gestion du champ «date_fin»
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
            // Si nous avons saisi de quoi de valide
            date_fin.style.background = "white";
            date_fin.style.border = "1px solid #ccc";
        }
        // Fin de la section du champ «date_debut»

        // On fait l'appel AJAX seulement si l'indication général est à false.
        if (!erreur_general){
            console.log("Yes !!!");
        }

    });

}

document.addEventListener('DOMContentLoaded', function () {
    // Cette fonction sera appellée lorsqu'on sort d'un champ à saisir des informations.
    validation_champs_recherches();
    recherche_rapide_par_interval();
});