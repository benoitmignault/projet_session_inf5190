// Variable pour le bouton Effacer dans la page de recherche
const recher_nom_resto = document.querySelector('#nom_resto');
const recher_nom_proprio = document.querySelector('#nom_proprio');
const recher_nom_rue = document.querySelector('#nom_rue');

// Variable pour effacer les messages
const message_aucun = document.querySelector('.aucun');

/*
    En fonction où nous sommes, sur le site, la fonction «re_initialiser_tous_champs» sera
    appelée pour chaque type de champs que le formulaire contient.
*/
function reset_recherche(){
    recher_nom_resto.defaultValue = "";
    recher_nom_proprio.defaultValue = "";
    recher_nom_rue.defaultValue = "";
    effacer_messages_erreurs();
}

function effacer_messages_erreurs(){
    // Nous devons vérifier que les variables ne sont pas égales à «undefined»
    if (message_aucun){
        message_aucun.innerHTML = "";
    }
}

function validation_champs_recherches(){
    var regex_resto = "^[a-z0-9 -'A-Z]{5,65}$";
    var regex_proprio = "^[a-z0-9 -'A-Z]{5,100}$";
    var regex_rue = "^[a-z0-9 -'A-Z]{1,35}$"

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

document.addEventListener('DOMContentLoaded', function () {
    // Cette fonction sera appellée lorsqu'on sort d'un champ à saisir des informations.
    validation_champs_recherches();
});