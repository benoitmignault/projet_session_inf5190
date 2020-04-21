// Variable pour la recherche par interval de date
const form_interval = document.querySelector('#recherche_par_interval');
const champ_date_debut = document.querySelector('#date_debut');
const champ_date_fin = document.querySelector('#date_fin');
const btn_reset_interval = document.querySelector('#btn_reset_interval');
const message_erreur_interval = document.querySelector('#message_erreur_interval');
const result_interval = document.querySelector('#result_interval');

// Variable pour la recherche par établissement précis après avoir sélectionner
const champ_liste_resto = document.querySelector('#liste_resto');
const result_interval_etablissement = document.querySelector('#result_interval_etablissement');

// Variables pour la recherche d'information générale pour être utiliser avec le bouton effacer
const form_recherche = document.querySelector('#recherche');
const champ_nom_resto = document.querySelector('#etablissement');
const champ_nom_proprio = document.querySelector('#proprietaire');
const champ_nom_rue = document.querySelector('#nom_rue');
const btn_reset_recher = document.querySelector('#btn_reset_recher');
const message_erreur_recher = document.querySelector('#message_erreur_recher');

// Variable pour l'ajout d'une demande de plainte
const form_nouvelle_plainte = document.querySelector('#nouvelle_plainte');
const btn_reset_plainte = document.querySelector('#btn_reset_plainte');
const message_erreur_plainte = document.querySelector('#message_erreur_plainte');
const result_plainte = document.querySelector('#result_plainte');
const champ_etablissement = document.querySelector('#etablissement');
const champ_no_civique = document.querySelector('#no_civique');
const champ_nom_rue_plainte = document.querySelector('#nom_rue');
const champ_nom_ville = document.querySelector('#nom_ville');
const champ_code_postal = document.querySelector('#code_postal');
const champ_date_visite = document.querySelector('#date_visite');
const champ_prenom_plaignant = document.querySelector('#prenom_plaignant');
const champ_nom_plaignant = document.querySelector('#nom_plaignant');
const champ_description = document.querySelector('#description');

// Variable pour la création du profil
const form_nouveau_profil = document.querySelector('#nouveau_profil');
const btn_reset_profil = document.querySelector('#btn_reset_profil');
const message_erreur_profil = document.querySelector('#message_erreur_profil');
const result_profil = document.querySelector('#result_profil');
const champ_prenom = document.querySelector('#prenom');
const champ_nom = document.querySelector('#nom');
const champ_courriel = document.querySelector('#courriel');
const champ_password = document.querySelector('#password');
const champ_password_conf = document.querySelector('#password_conf');
// Les variables de la liste des établissements seront crée au besoin

// Variable pour la connection au profil
const form_connection_profil = document.querySelector('#connection_profil');
const btn_reset_connection = document.querySelector('#btn_reset_connection');
const message_erreur_connection = document.querySelector('#message_erreur_connection');
const champ_courriel_connection = document.querySelector('#courriel_conn');
const champ_password_connection = document.querySelector('#password_conn');

// Variable commune pour les deux appels ajax de la section des établissements + photo
const tableau_etablissement = document.querySelector('.tableau_profil');
const list_etablissement_dispo = document.querySelector('#ajout_resto_profil');
const champ_id_personne = document.querySelector('#id_personne');

// Variable pour la gestion des établissements du profil
const form_ajout_etablissement = document.querySelector('#ajout_etablissement');
const btn_reset_etablissement = document.querySelector('#btn_reset_etablissement');
const message_erreur_etablissement = document.querySelector('#message_erreur_etablissement');

// Variable pour retirer un établissement de la liste de surveillance
const form_retrait_etablissement = document.querySelector('#retrait_etablissement');

// Variable pour gérer la photo de profile
const form_gestion_photo = document.querySelector('#nouvelle_photo');
const champ_fichier_photo = document.querySelector('#photo');
const champ_btn_ajout_photo = document.querySelector('#ajout');
const champ_btn_modifier_photo = document.querySelector('#modifier');
const champ_btn_supprimer_photo = document.querySelector('#supprimer');
const champ_id_photo = document.querySelector('#id_photo');
const section_photo_profil = document.querySelector('.unePassionPhoto');

const pattern_date = new RegExp("^([0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])$");
const pattern_code = new RegExp("^[A-Z][0-9][A-Z][ ]{1}[0-9][A-Z][0-9]$");
const pattern_proprio = new RegExp("^[a-z1-9A-Z][a-z0-9- 'A-Z@_!#$%^&*()<>?/\\|}{~:]{3,98}[a-z0-9A-Z.)]$");
const pattern_ville = new RegExp("^[a-z1-9A-Z][a-z0-9- 'A-Z@_!#$%^&*()<>?/\\|}{~:]{3,31}[a-z0-9A-Z.)]$");
const pattern_rue = new RegExp("^[a-z1-9A-Z][a-z0-9- 'A-Z]{1,33}[a-z0-9A-Z]$");
const pattern_courriel = new RegExp("^([a-zA-Z0-9_\\.\\-\\+])+\\@(([a-zA-Z0-9\\-])+\\.)+([a-zA-Z0-9]{2,4})+$");
const pattern_prenom_nom = new RegExp("^[A-Z][a-z-A-Z]{1,48}[a-z]$");
const pattern_password = new RegExp("^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[@$!%*()?&])[A-Za-z\\d@()$!%*?&]{8,20}$");

// Cette fonction sera pour la tache D1
function initial_plainte_validation(){
    var liste_validation = {"champ_etablissement_vide": false, "champ_numero_vide": false,
        "champ_numero_inv": false, "champ_rue_vide": false, "champ_ville_vide": false,
        "champ_code_vide": false, "champ_code_inv": false, "champ_date_vide": false,
        "champ_date_inv": false, "champ_prenom_vide": false, "champ_nom_vide": false,
        "champ_prenom_inv": false, "champ_nom_inv": false, "champ_description_vide": false, "champ_rue_inv": false,
        "champ_ville_inv": false, "requete_ajax_avec_erreur": false};

    return liste_validation;
}

// Cette fonction sera pour la tache E2
function initial_profil_validation(){
    var liste_validation = {"champ_prenom_vide": false, "champ_nom_vide": false,
        "champ_prenom_inv": false, "champ_nom_inv": false, "champ_courriel_vide": false,
        "champ_password_vide": false, "champ_password_conf_vide": false,
        "champ_courriel_inv": false, "champ_password_inv": false, "champ_password_conf_inv": false,
        "champ_passwords_non_egal": false, "requete_ajax_avec_erreur": false,
        "champ_liste_resto_profil_vide": false};

    return liste_validation;
}

// Cette fonction sera pour la tache E2
function initial_connection_validation(){
    var liste_validation = {"champ_courriel_vide": false, "champ_password_vide": false,
        "champ_courriel_inv": false, "champ_password_inv": false, "erreur_formulaire": false};

    return liste_validation;
}

// Cette fonction sera pour la tache A2
function initial_recherche_validation(){
    var liste_validation = {"aucune_recherche": false,"champ_proprio_inv": false,
        "champ_rue_inv": false, "erreur_formulaire": false};

    return liste_validation;
}

// Cette fonction sera pour la tache A5 et A6
function initial_recherche_interval_validation(){
    var liste_validation = {"champ_debut_inv": false, "aucun_choix": false,
        "champ_fin_inv": false, "champ_debut_vide": false, "champ_fin_vide": false,
        "champ_liste_resto_vide": false, "les_deux_choix": false, "champs_date_vides": false};

    return liste_validation;
}

// Cette fonction sera pour la tache A2
// Récupérer comment désecltionner mardi de la job
function reset_recherche(){
    $(btn_reset_recher).click(function() {
        champ_nom_proprio.defaultValue = "";
        champ_nom_rue.defaultValue = "";
        champ_nom_resto.options.selectedIndex = 0; // marche pas
        effacer_messages_erreurs(message_erreur_recher);
        initialiser_tous_champs("#etablissement, #proprietaire, #nom_rue, #recherche");
    });
}

// Cette fonction sera pour la tache A5
function reset_recherche_interval(){
    $(btn_reset_interval).click(function() {
        champ_date_debut.defaultValue = "";
        champ_date_fin.defaultValue = "";
        result_interval.innerHTML = "";
        result_interval_etablissement.innerHTML = "";
        effacer_messages_erreurs(message_erreur_interval);
        initialiser_tous_champs("#date_debut, #date_fin, #liste_resto, #recherche_par_interval");
    });
}

// Cette fonction sera pour la tache D1
function reset_demande_plainte(){
    $(btn_reset_plainte).click(function() {
        champ_etablissement.defaultValue = "";
        champ_no_civique.defaultValue = "";
        champ_nom_rue_plainte.defaultValue = "";
        champ_nom_ville.defaultValue = "";
        champ_code_postal.defaultValue = "";
        champ_date_visite.defaultValue = "";
        champ_prenom_plaignant.defaultValue = "";
        champ_nom_plaignant.defaultValue = "";
        champ_description.defaultValue = "";
        result_plainte.innerHTML = "";
        effacer_messages_erreurs(message_erreur_plainte);
        initialiser_tous_champs("#nouvelle_plainte, input[type=text]");
    });
}

// Cette fonction sera pour la tache E2
function reset_nouveau_profil(){
    $(btn_reset_profil).click(function() {
        champ_prenom.defaultValue = "";
        champ_nom.defaultValue = "";
        champ_courriel.defaultValue = "";
        champ_password.defaultValue = "";
        champ_password_conf.defaultValue = "";
        initialiser_selection_evoluee();
        effacer_messages_erreurs(message_erreur_profil);
        initialiser_tous_champs("input[type=password], input[type=email], input[type=text], #nouveau_profil");
    });
}

// Cette fonction sera pour la tache E2
function reset_demande_connection(){
    $(btn_reset_connection).click(function() {
        champ_courriel_connection.defaultValue = "";
        champ_password_connection.defaultValue = "";
        effacer_messages_erreurs(message_erreur_connection);
        initialiser_tous_champs("input[type=email], input[type=password], #connection_profil");
    });
}

// Cette fonction sera pour la tache E2
function reset_gestion_etablissement(){
    $(btn_reset_etablissement).click(function() {
        effacer_messages_erreurs(message_erreur_etablissement);
        initialiser_selection_evoluee();
    });
}

// Cette fonction sera pour la tache E2
function initialiser_selection_evoluee(){
    $('.select2-selection__rendered .select2-selection__choice').each(function () {
            $(this).remove(); // Remove li one by one
    });
    // Champ où est affiché la liste sans être la liste
    var champ_liste_etablissement = document.querySelector('.select2-search__field');
    var section_afficher_liste = document.querySelector('.select2-search--inline');
    // Remise aux valeurs initiales du champ
    champ_liste_etablissement.placeholder = "Choix d'(es) établissement(s)";
    section_afficher_liste.style.width = "100%";
    champ_liste_etablissement.style.width = "100%";
}

// Cette fonction sera pour toutes les taches qui possèdent une interface web
function initialiser_tous_champs(type_champs){
    var tous_champs = document.querySelectorAll(type_champs);
    tous_champs.forEach(function(un_champ){
        if (un_champ.localName == "form"){
            un_champ.style.border = "2px solid black";
        } else {
            un_champ.style.backgroundColor = "white";
            un_champ.style.border = "1px solid #ccc";
        }
    });
}

// Fonction utilisée pour retirer les messages d'erreurs de la secteur seulement si elle existe
function effacer_messages_erreurs(message){
    if (message){
        message.innerHTML = "";
    }
}

// Cette fonction sera pour la tache A2 à des fins de validations
function recherche(){
    $(form_recherche).submit(function (e) {
        message_erreur_recher.innerHTML = "";
        var liste_validation = initial_recherche_validation();
        liste_validation = verification_recherche(liste_validation);
        message_erreur_recherche(liste_validation);
        ajustement_style_champs_rech(liste_validation);
        liste_validation = verification_evocation_non_ajax(liste_validation);
        if (liste_validation['erreur_formulaire']){
            e.preventDefault();
        }
    });
}

// Cette fonction sera pour la tache A5 et A6 à des fins de validations et d'appel Ajax
function recherche_rapide(){
    $(form_interval).submit(function (e) {
        e.preventDefault();
        message_erreur_interval.innerHTML = ""; //
        var liste_validation = initial_recherche_interval_validation();
        liste_validation = verification_interval(liste_validation);
        liste_validation = verification_choix_etablissement(liste_validation);
        message_erreur_recherche_rapide(liste_validation);
        ajustement_style_champs_rech_rapide(liste_validation);
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

// Cette fonction sera pour la tache D1 à des fins de validations et d'appel Ajax
function demande_plainte(){
    $(form_nouvelle_plainte).submit(function (e) {
        e.preventDefault();
        message_erreur_plainte.innerHTML = "";
        var liste_validation = initial_plainte_validation();
        liste_validation = verification_nouvelle_plainte(liste_validation);
        message_erreur_nouvelle_plainte(liste_validation);
        liste_validation = verification_evocation_ajax(liste_validation);
        if (!liste_validation['requete_ajax_avec_erreur']){
            appel_ajax_nouvelle_plainte();
        }
    });
}

// Cette fonction sera pour la tache E2 à des fins de validations et d'appel Ajax
function demande_nouveau_profil(){
    $(form_nouveau_profil).submit(function (e) {
        e.preventDefault();
        message_erreur_profil.innerHTML = "";
        var liste_validation = initial_profil_validation();
        liste_validation = verification_nouveau_profil(liste_validation);
        message_erreur_nouveau_profil(liste_validation);
        liste_validation = verification_evocation_ajax(liste_validation);
        if (!liste_validation['requete_ajax_avec_erreur']){
            // Il se pourrait que la requête précédente était invalide
            initialiser_tous_champs("#nouveau_profil");
            appel_ajax_nouveau_profil();
        }
    });
}

// Cette fonction sera pour la tache E2 à des fins de validations
function demande_connection_profil(){
    $(form_connection_profil).submit(function (e) {
        message_erreur_connection.innerHTML = "";
        var liste_validation = initial_connection_validation();
        liste_validation = verification_connection_profil(liste_validation);
        message_erreur_nouvelle_connection(liste_validation);
        liste_validation = verification_evocation_non_ajax(liste_validation);
        if (liste_validation['erreur_formulaire']){
            e.preventDefault();
        }
    });
}

// Cette fonction sera pour la tache E2 pour un call Ajax
function retrait_etablissement_profil(){
    $(form_retrait_etablissement).submit(function (e) {
        e.preventDefault();
        // Ça permet de récupérer l'informartion du bouton sélectionner
        var $btn = $(document.activeElement);
        var id_surveillance = $btn.attr("id")
        appel_ajax_retrait_etablissement_profil(id_surveillance);
    });
}

// Cette fonction sera pour la tache E2 à des fins de validations et d'appel Ajax
function ajout_etablissements_profil(){
    $(form_ajout_etablissement).submit(function (e) {
        e.preventDefault();
        var liste_etablissements = document.querySelectorAll('.select2-selection__choice');
        if (liste_etablissements.length == 0){
            alert("Veuiller saisir une liste établissements à surveiller !");
        } else {
            appel_ajax_ajout_etablissement_profil(liste_etablissements);
        }
    });
}

// Cette fonction sera pour la tache E2 à des fins de validations et d'appel Ajax pour la gestion de la photo de profil
function ajout_modif_retrait_photo_profil(){
    $(form_gestion_photo).on('submit', function(e) {
    var $btn = $(document.activeElement);

    if ( $(champ_fichier_photo).get(0).files.length == 0 && $btn.attr("name") === "supprimer"){
        e.preventDefault();
        appel_ajax_supprimer_photo_profil();

    } else if ( $(champ_fichier_photo).get(0).files.length == 1 && $btn.attr("name") === "supprimer"){
        e.preventDefault();
        alert("Attention ! Au moment de détruire votre photo de profil, veuiller à ne pas sélectionner de nouvelle !");

    } else {
        if ( $(champ_fichier_photo).get(0).files.length == 0 ){
            e.preventDefault();
            alert("Veuiller sélectionner un fichier pour votre photo de profile !");
        }
    }
    });
}

// Cette fonction sera pour la tache E2 à des fins de validations pour vérifier l'état des boutons
function validation_bouton_section_photo(){
    if (champ_id_photo){
        if (champ_id_photo.value == "None"){
            activation_bouton(champ_btn_ajout_photo);
            desactivation_bouton(champ_btn_modifier_photo);
            desactivation_bouton(champ_btn_supprimer_photo);
        } else {
            activation_bouton(champ_btn_modifier_photo);
            activation_bouton(champ_btn_supprimer_photo);
            desactivation_bouton(champ_btn_ajout_photo);
        }
    }
}

// Sous fonction de validation_bouton_section_photo
function activation_bouton(champ){
    champ.setAttribute("class", "bouton");
    champ.removeAttribute("disabled");
    champ.style.backgroundImage = "linear-gradient(to bottom, #507d99, #96cceb";
}

// Sous fonction de validation_bouton_section_photo
function desactivation_bouton(champ){
    champ.setAttribute("class", "bouton disabled");
    champ.setAttribute("disabled", "disabled");
    champ.style.background = "darkgray";
}

// Cette fonction sera pour la tache A2
function verification_recherche(liste_validation){
    if (champ_nom_resto.value == "" && champ_nom_proprio.value == "" && champ_nom_rue.value == "") {
        liste_validation['aucune_recherche'] = true;
    } else {
        if (champ_nom_proprio.value != ""){
            if (!(pattern_proprio.test(champ_nom_proprio.value))) {
                liste_validation['champ_proprio_inv'] = true;
            }
        }

        if (champ_nom_rue.value != ""){
            if (!(pattern_rue.test(champ_nom_rue.value))) {
                liste_validation['champ_rue_inv'] = true;
            }
        }
    }

    return liste_validation;
}

// Cette fonction sera pour la tache A5
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

// Cette fonction sera pour la tache A5 et A6
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

// Cette fonction sera pour la tache D2
function verification_nouvelle_plainte(liste_validation){
    verification_champs_vides(); // Parce que tous les champs doivent être remplis

    if (champ_etablissement.options.selectedIndex == 0) {
        liste_validation['champ_etablissement_vide'] = true;
    }

    if (champ_no_civique.value == "") {
        liste_validation['champ_numero_vide'] = true;
    } else if (isNaN(champ_no_civique.value)){
	        liste_validation['champ_numero_inv'] = true;
	}

    if (champ_nom_rue_plainte.value == "") {
        liste_validation['champ_rue_vide'] = true;
    } else if (!(pattern_rue.test(champ_nom_rue_plainte.value))){
	    liste_validation['champ_rue_inv'] = true;
    }

    if (champ_nom_ville.value == "") {
        liste_validation['champ_ville_vide'] = true;
    } else if (!(pattern_rue.test())){
	    liste_validation['champ_ville_inv'] = true;
    }

    if (champ_code_postal.value == "") {
        liste_validation['champ_code_vide'] = true;
    } else if (!(pattern_code.test(champ_code_postal.value.toUpperCase()))){
	    liste_validation['champ_code_inv'] = true;
    }

    if (champ_date_visite.value == "") {
        liste_validation['champ_date_vide'] = true;
    } else if (!(pattern_date.test(champ_date_visite.value))){
	    liste_validation['champ_date_inv'] = true;
    }

    if (champ_prenom_plaignant.value == "") {
        liste_validation['champ_prenom_vide'] = true;
    } else if (!(pattern_prenom_nom.test(champ_prenom_plaignant.value))){
	    liste_validation['champ_prenom_inv'] = true;
    }

    if (champ_nom_plaignant.value == "") {
        liste_validation['champ_nom_vide'] = true;
    } else if (!(pattern_prenom_nom.test(champ_nom_plaignant.value))){
	    liste_validation['champ_nom_inv'] = true;
    }

    if (champ_description.value == "") {
        liste_validation['champ_description_vide'] = true;
    }

    return liste_validation;
}

// Cette fonction sera pour la tache E2 pour créer un profil
function verification_nouveau_profil(liste_validation){
    verification_champs_vides();

    if (champ_prenom.value == "") {
        liste_validation['champ_prenom_vide'] = true;
    } else if(!(pattern_prenom_nom.test(champ_prenom.value))){
	    liste_validation['champ_prenom_inv'] = true;
    }

    if (champ_nom.value == "") {
        liste_validation['champ_nom_vide'] = true;
    } else if(!(pattern_prenom_nom.test(champ_nom.value))){
	    liste_validation['champ_nom_inv'] = true;
    }

    if (champ_courriel.value == "") {
        liste_validation['champ_courriel_vide'] = true;
    } else if(!(pattern_courriel.test(champ_courriel.value))){
	    liste_validation['champ_courriel_inv'] = true;
    }

    if (champ_password.value == "") {
        liste_validation['champ_password_vide'] = true;
    } else if(!(pattern_password.test(champ_password.value))){
	    liste_validation['champ_password_inv'] = true;
    }

    if (champ_password_conf.value == "") {
        liste_validation['champ_password_conf_vide'] = true;
    } else if(!(pattern_password.test(champ_password_conf.value))){
	    liste_validation['champ_password_conf_inv'] = true;
    }

    if (!liste_validation['champ_password_vide'] && !liste_validation['champ_password_conf_vide']){
        if (champ_password.value.localeCompare(champ_password_conf.value) != 0){
            liste_validation['champ_passwords_non_egal'] = true;
        }
    }

    // En fonction de la manière que fonctionne Select2 de Jquery,
    // je dois compter le nombre de li dans le ul de la classe selection__rendered
    // 1 équivaut au LI de base
    if ($('.select2-selection__rendered li').length == 1){
        liste_validation['champ_liste_resto_profil_vide'] = true;
    }

    return liste_validation;
}

// Cette fonction sera pour la tache E2 pour se connecter
function verification_connection_profil(liste_validation){
    if (champ_courriel_connection.value == "") {
        liste_validation['champ_courriel_vide'] = true;
    } else if(!(pattern_courriel.test(champ_courriel_connection.value))){
	    liste_validation['champ_courriel_inv'] = true;
    }

    if (champ_password_connection.value == "") {
        liste_validation['champ_password_vide'] = true;
    } else if(!(pattern_password.test(champ_password_connection.value))){
	    liste_validation['champ_password_inv'] = true;
    }

    return liste_validation;
}

// Cette fonction sera pour la tache D2 et E2
// en raison du grand nombre de champs obligatoiresw à saisir
// Nous avons pris la décision de faire un message générique pour les champs vides
function verification_champs_vides(){
    // Une manière simple d'afficher un message générale, s'il y a des champs vides
    // https://stackoverflow.com/questions/16211871/how-to-check-if-all-inputs-are-not-empty-with-jquery
    $('input[type=text]').each(function() {
        if (!$(this).val()){
            if (this.hasAttribute('placeholder') && ( this.placeholder !== "Choix d'(es) établissement(s)" || this.placeholder !== "À Sélectionner") ){
                return true;
            } else {
                alert('Attention ! Il y a encore des champs vides !');
                return false;
            }
        }
    });
}

// Cette fonction sera pour déterminer si on doit bloquer l'envoi du formulaire à la route Flask prévue
function verification_evocation_non_ajax(liste_validation){
    for (var key in liste_validation) {
        if (liste_validation[key]){
            liste_validation['erreur_formulaire'] = true;
            break;
        }
    }

    return liste_validation;
}

// Cette fonction sera pour déterminer si on doit bloquer l'appel AJAX
function verification_evocation_ajax(liste_validation){
    for (var key in liste_validation) {
        if (liste_validation[key]){
            liste_validation['requete_ajax_avec_erreur'] = true;
            break;
        }
    }

    return liste_validation;
}

// Cette fonction sera pour la tache A2
function message_erreur_recherche(liste_validation){
    if (liste_validation['aucune_recherche']){
            message_erreur_recher.innerHTML += "<li>Vous devez remplir au moins un des trois critères !</li>";
    } else {
        if (liste_validation['champ_proprio_inv']){
            message_erreur_recher.innerHTML += "<li>Veuillez respecter les charactères permis et la longueur permise !</li>";
        }

        if (liste_validation['champ_rue_inv']){
            message_erreur_recher.innerHTML += "<li>Veuillez respecter les charactères permis et la longueur permise !</li>";
        }
    }
}

// Cette fonction sera pour la tache A5 et A6
function message_erreur_recherche_rapide(liste_validation){
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

// Cette fonction sera pour la tache D1
// Cette ne peut pas faire 25 lignes vue le nombre de messages d'erreurs possible
function message_erreur_nouvelle_plainte(liste_validation){
    if (liste_validation['champ_numero_inv']) {
        message_erreur_plainte.innerHTML += "<li>Veuillez saisir un numéro civique numériquement !</li>";
        modification_erreur_champs_selectionner('#no_civique');
    } else {
        modification_correct_champs_selectionner('#no_civique');
    }

    if (liste_validation['champ_rue_inv']) {
        message_erreur_plainte.innerHTML += "<li>Votre rue doit respecter les charactères permis et la longueur permise !</li>";
        modification_erreur_champs_selectionner('#nom_rue');
    } else {
        modification_correct_champs_selectionner('#nom_rue');
    }

    if (liste_validation['champ_ville_inv']) {
        message_erreur_plainte.innerHTML += "<li>Votre ville doit respecter les charactères permis et la longueur permise !</li>";
        modification_erreur_champs_selectionner('#nom_ville');
    } else {
        modification_correct_champs_selectionner('#nom_ville');
    }

    if (liste_validation['champ_code_inv']) {
        message_erreur_plainte.innerHTML += "<li>Votre code postal doit respecter le format H1H 1H1 !</li>";
        modification_erreur_champs_selectionner('#code_postal');
    } else {
        modification_correct_champs_selectionner('#code_postal');
    }

    if (liste_validation['champ_date_inv']) {
        message_erreur_plainte.innerHTML += "<li>La date de la plainte doit être au format ISO 8601 !</li>";
        modification_erreur_champs_selectionner('#date_visite');
    } else {
        modification_correct_champs_selectionner('#date_visite');
    }

    if (liste_validation['champ_prenom_inv']) {
        message_erreur_plainte.innerHTML += "<li>Votre prénom doit respecter les charactères permis et la longueur permise !</li>";
        modification_erreur_champs_selectionner('#prenom_plaignant');
    } else {
        modification_correct_champs_selectionner('#prenom_plaignant');
    }

    if (liste_validation['champ_nom_inv']) {
        message_erreur_plainte.innerHTML += "<li>Votre nom doit respecter les charactères permis et la longueur permise !</li>";
        modification_erreur_champs_selectionner('#nom_plaignant');
    } else {
        modification_correct_champs_selectionner('#nom_plaignant');
    }
}

// Cette fonction sera pour la tache E2
// Cette ne peut pas faire 25 lignes vue le nombre de messages d'erreurs possible
function message_erreur_nouveau_profil(liste_validation){
    if (liste_validation['champ_prenom_inv']) {
        message_erreur_profil.innerHTML += "<li>Veuillez saisir un prenom valide allant jusqu'à 50 charactères !</li>";
        modification_erreur_champs_selectionner('#prenom');
    } else {
        modification_correct_champs_selectionner('#prenom');
    }

    if (liste_validation['champ_nom_inv']) {
        message_erreur_profil.innerHTML += "<li>Veuillez saisir un nom valide allant jusqu'à 50 charactères !</li>";
        modification_erreur_champs_selectionner('#nom');
    } else {
        modification_correct_champs_selectionner('#nom');
    }

    if (liste_validation['champ_courriel_inv']) {
        message_erreur_profil.innerHTML += "<li>Veuillez saisir un courriel qui respect «exemple@domaine.com» !</li>";
        modification_erreur_champs_selectionner('#courriel');
    } else {
        modification_correct_champs_selectionner('#courriel');
    }

    if (liste_validation['champ_password_inv']) {
        message_erreur_profil.innerHTML += "<li>Veuillez saisir un mot de passe valide allant de 8 et 20 charactères !</li>";
    }

    if (liste_validation['champ_password_conf_inv']) {
        message_erreur_profil.innerHTML += "<li>Veuillez saisir la confirmation du mot de passe valide allant de 8 et 20 charactères !</li>";
    }

    if (liste_validation['champ_passwords_non_egal']){
        message_erreur_profil.innerHTML += "<li>Veuillez saisir un mot de passe et sa confirmatinon identique !</li>";
    }

    if (liste_validation['champ_password_inv'] && liste_validation['champ_passwords_non_egal']){
        modification_erreur_champs_selectionner('#password');
    } else {
        modification_correct_champs_selectionner('#password');
    }

    if (liste_validation['champ_password_conf_inv'] && liste_validation['champ_passwords_non_egal']){
        modification_erreur_champs_selectionner('#password_conf');
    } else {
        modification_correct_champs_selectionner('#password_conf');
    }
}

// Cette fonction sera pour la tache E2
function message_erreur_nouvelle_connection(liste_validation){
    if (liste_validation['champ_courriel_vide'] && liste_validation['champ_password_vide']){
        message_erreur_connection.innerHTML += "<li>Veuillez saisir un courriel et un mot de passe, afin de vous connectez !</li>";
        modification_erreur_champs_selectionner('#courriel_conn, #password_conn');
    } else {
        if (liste_validation['champ_courriel_vide']) {
            message_erreur_connection.innerHTML += "<li>Veuillez saisir un courriel !</li>";
            modification_erreur_champs_selectionner('#courriel_conn');
        } else if (liste_validation['champ_courriel_inv']) {
            message_erreur_connection.innerHTML += "<li>Veuillez saisir un courriel qui respect «exemple@domaine.com» !</li>";
            modification_erreur_champs_selectionner('#courriel_conn');
        } else {
            modification_correct_champs_selectionner('#courriel_conn');
        }

        if (liste_validation['champ_password_vide']) {
            message_erreur_connection.innerHTML += "<li>Veuillez saisir un mot de passe !</li>";
            modification_erreur_champs_selectionner('#password_conn');
        } else if (liste_validation['champ_password_inv']) {
            message_erreur_connection.innerHTML += "<li>Veuillez saisir un mot de passe valide allant de 8 et 20 charactères !</li>";
            modification_erreur_champs_selectionner('#password_conn');
        } else {
            modification_correct_champs_selectionner('#password_conn');
        }
    }
}

// Cette fonction sera pour les champs qui ont recu un tag d'erreur
function modification_erreur_champs_selectionner(champs){
    var tous_champs = document.querySelectorAll(champs);
    tous_champs.forEach(function(un_champ){
        un_champ.style.border = "2px solid red";
        un_champ.style.backgroundColor = "#FCDEDE";
    });
}

// Cette fonction sera pour les champs qui ont recu un tag correct
function modification_correct_champs_selectionner(champs){
    var tous_champs = document.querySelectorAll(champs);
    tous_champs.forEach(function(un_champ){
        un_champ.style.border = "1px solid #ccc";
        un_champ.style.backgroundColor = "white";
    });
}

// Cette fonction sera pour la tache A2
// Cette fonction appellera les sous fonction
// modification_erreur_champs_selectionner -> pour un champ en erreur
// modification_erreur_champs_selectionner -> pour un champ correct
function ajustement_style_champs_rech(liste_validation){
    if (liste_validation['aucune_recherche']){
        modification_erreur_champs_selectionner("#etablissement, #proprietaire, #nom_rue");
    } else {
        if (liste_validation['champ_proprio_inv']){
            modification_erreur_champs_selectionner("#proprietaire");
        } else {
            modification_correct_champs_selectionner("#proprietaire");
        }

        if (liste_validation['champ_rue_inv']){
            modification_erreur_champs_selectionner("#nom_rue");
        } else {
            modification_correct_champs_selectionner("#nom_rue");
        }
    }
}

// Cette fonction sera pour la tache A5, A6
// Cette fonction appellera les sous fonction
// modification_erreur_champs_selectionner -> pour un champ en erreur
// modification_erreur_champs_selectionner -> pour un champ correct
function ajustement_style_champs_rech_rapide(liste_validation){
    if (liste_validation['champ_debut_inv'] || (liste_validation['champ_debut_vide'] && liste_validation['champ_liste_resto_vide'])){
        modification_erreur_champs_selectionner("#date_debut");
    } else {
        modification_correct_champs_selectionner("#date_debut");
    }

    if (liste_validation['champ_fin_inv'] || (liste_validation['champ_fin_vide'] && liste_validation['champ_liste_resto_vide'])){
        modification_erreur_champs_selectionner("#date_fin");
    } else {
        modification_correct_champs_selectionner("#date_fin");
    }

    if (liste_validation['champ_liste_resto_vide'] && (liste_validation['aucun_choix'] || liste_validation['les_deux_choix'])){
        modification_erreur_champs_selectionner("#liste_resto");
    } else {
        modification_correct_champs_selectionner("#liste_resto");
    }

    if (liste_validation['aucun_choix'] || liste_validation['les_deux_choix']){

        modification_erreur_champs_selectionner("#date_debut, #date_fin, #liste_resto");
        form_interval.style.border = "2px solid red";
    } else {
        form_interval.style.border = "2px solid black";
    }
}

// Cette fonction est l'appel Ajax pour A5
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
                    appel_ajax_erreur(result_interval, form_interval, message_erreur_interval, "<li>L'interval de date ne contenait aucune donnée !</li>");
                }
            } else {
                appel_ajax_erreur(result_interval, form_interval, message_erreur_interval, "<li>Attention ! Il y a eu une erreur avec la réponse du serveur !</li>");
            }
        }
    };
    var date_debut_encode = encodeURIComponent(champ_date_debut.value);
    var date_fin_encode = encodeURIComponent(champ_date_fin.value);
    var param = `?du=${date_debut_encode}&au=${date_fin_encode}`;
    ajax.open("POST", "/api/liste_des_contrevenants/interval" + param, true);
    ajax.send();
}

// Cette fonction est l'appel Ajax pour A6
function appel_ajax_interval_etablissement(){
    var ajax = new XMLHttpRequest();
    ajax.onreadystatechange = function() {
        if (ajax.readyState === XMLHttpRequest.DONE) {
            if (ajax.status === 200) {
                var liste = JSON.parse(ajax.responseText);
                result_interval_etablissement.innerHTML = creation_bloc_html_etablissement(liste);
            } else {
                appel_ajax_erreur(result_interval, form_interval, message_erreur_interval, "<li>Attention ! Il y a eu une erreur avec la réponse du serveur !</li>");
            }
        }
    };
    var nom_encode = encodeURIComponent(champ_liste_resto.value);
    var param = `?choix=${nom_encode}`;
    ajax.open("GET", "/api/liste_des_contrevenants/etablissement" + param, true);
    ajax.send();
}

// Cette fonction est l'appel Ajax pour D1
function appel_ajax_nouvelle_plainte(){
    var ajax = new XMLHttpRequest();
    ajax.onreadystatechange = function() {
        if (ajax.readyState === XMLHttpRequest.DONE) {
            if (ajax.status === 201) {
                var liste = JSON.parse(ajax.responseText);
                result_plainte.innerHTML = creation_bloc_html(liste);
            } else {
                message_erreur_plainte.innerHTML += "<li>Attention ! Il y a eu une erreur avec la réponse du serveur !</li>";
                appel_ajax_erreur(result_plainte, nouvelle_plainte, message_erreur_plainte, "<li>Attention ! Il y a eu une erreur avec la réponse du serveur !</li>");
            }
        }
    };
    var data = {
            "etablissement": champ_etablissement.value,
            "no_civique": parseInt(champ_no_civique.value),
            "nom_rue": champ_nom_rue_plainte.value,
            "ville": champ_nom_ville.value + " " + champ_code_postal.value,
            "date_visite": champ_date_visite.value,
            "prenom_plaignant": champ_prenom_plaignant.value,
            "nom_plaignant": champ_nom_plaignant.value,
            "description": champ_description.value
        };
    var data_json = JSON.stringify(data);
    ajax.open("POST", "/api/nouvelle_plainte", true);
    ajax.setRequestHeader("Content-Type", "application/json");
    ajax.send(data_json);
}

// Cette fonction est l'appel Ajax pour E2
function appel_ajax_nouveau_profil(){
    var ajax = new XMLHttpRequest();
    ajax.onreadystatechange = function() {
        if (ajax.readyState === XMLHttpRequest.DONE) {
            if (ajax.status === 201) {
                var liste = JSON.parse(ajax.responseText);
                message_erreur_profil.innerHTML = creation_bloc_html(liste);
            } else{
                message_erreur = "";
                if (ajax.status === 404)  {
                    message_erreur = "<li>Impossible de créer le profil, car le Courriel est déjà présent !</li>";
                } else {
                    message_erreur = "<li>Attention ! Il y a eu une erreur avec la réponse du serveur !</li>";
                }
                appel_ajax_erreur(result_profil, form_nouveau_profil, message_erreur_profil, message_erreur);
            }
        }
    };
    var data = {
            "nom": champ_nom.value,
            "prenom": champ_prenom.value,
            "courriel": champ_courriel.value,
            "password": champ_password.value,
            "liste_etablissement": []
    };
    var liste_etablissements = document.querySelectorAll('.select2-selection__choice');
    liste_etablissements.forEach(function(un_etablissement){
        data["liste_etablissement"].push(un_etablissement.title.trim());
    });

    var data_json = JSON.stringify(data);
    ajax.open("POST", "/api/nouveau_profil", true);
    ajax.setRequestHeader("Content-Type", "application/json");
    ajax.send(data_json);
}

// Cette fonction est l'appel Ajax pour E2
function appel_ajax_ajout_etablissement_profil(liste_etablissements){
    var ajax = new XMLHttpRequest();
    ajax.onreadystatechange = function() {
        if (ajax.readyState === XMLHttpRequest.DONE) {
            if (ajax.status === 200) {
                var liste = JSON.parse(ajax.responseText);
                refaire_tableau_etablissement(liste["etablissement"]);
                refaire_etablissement_disponible(liste["etablissement_dispo"]);
            } else {
                message_erreur_etablissement.innerHTML += "<li>Attention ! Il y a eu une erreur avec la réponse du serveur !</li>";
            }
        }
    };

    var data = {
            "id_personne": parseInt(champ_id_personne.value),
            "liste_etablissement": []
    };

    liste_etablissements.forEach(function(un_etablissement){
        data["liste_etablissement"].push(un_etablissement.title.trim());
    });

    var data_json = JSON.stringify(data);
    ajax.open("POST", "/api/connecter/ajouter_etablissement", true);
    ajax.setRequestHeader("Content-Type", "application/json");
    ajax.send(data_json);
}

// Cette fonction est l'appel Ajax pour E2
function appel_ajax_retrait_etablissement_profil(id_surveillance){
    var ajax = new XMLHttpRequest();
    ajax.onreadystatechange = function() {
        if (ajax.readyState === XMLHttpRequest.DONE) {
            if (ajax.status === 200) {
                var liste = JSON.parse(ajax.responseText);
                supprimer_ligne_tableau_etablissement(id_surveillance);
                refaire_etablissement_disponible(liste);
            }
        }
    };
    var data = {
            "id_surveillance": parseInt(id_surveillance),
            "id_personne": parseInt(champ_id_personne.value)
    };

    var data_json = JSON.stringify(data);
    ajax.open("DELETE", "/api/connecter/retirer_etablissement", true);
    ajax.setRequestHeader("Content-Type", "application/json");
    ajax.send(data_json);
}

// Cette fonction est l'appel Ajax pour E2
function appel_ajax_supprimer_photo_profil(){
    var ajax = new XMLHttpRequest();
    ajax.onreadystatechange = function() {
        if (ajax.readyState === XMLHttpRequest.DONE) {
            if (ajax.status === 200) {
                champ_id_photo.value = "None";
                section_photo_profil.innerHTML = "";
                validation_bouton_section_photo();
            } else if (ajax.status === 404) {
                alert("Attention ! La photo que vous tentez de supprimer n'existe déjà plus !");
            }
        }
    };
    var data = {
            "id_photo": champ_id_photo.value,
            "id_personne": parseInt(champ_id_personne.value)
    };

    var data_json = JSON.stringify(data);
    ajax.open("DELETE", "/api/connecter/supprimer_photo", true);
    ajax.setRequestHeader("Content-Type", "application/json");
    ajax.send(data_json);
}

// Cette fonction servira à refaire la lsite des établissements après l'appel AJAX
function refaire_etablissement_disponible(liste){
    // On supprime toutes les vieilles options
    $(list_etablissement_dispo).empty();
    for(var i = 0; i < liste.length; i++) {
        var option = liste[i];
        // Pour refaire toutes les options MAJ en fonction de l'ajout ou du retrait
        $(list_etablissement_dispo).append(new Option(option, option));
    }
}

// Cette fonction servira à refaire la liste des établissements après l'appel AJAX
function refaire_tableau_etablissement(liste){
    $(tableau_etablissement).find("tr:gt(0)").remove();
    for(var i = 0; i < liste.length; i++) {
        const un_etablissement = Object.entries(liste[i]);
        var id_surveillance = 0;
        var etablissement = "";
        for (const [cle, valeur] of un_etablissement) {
            if (cle == "id_surveillance"){
                id_surveillance = valeur;
            } else if (cle == "nom"){
                etablissement = valeur;
            }
        }
        var nouvelle_ligne = "<tr class=\""+id_surveillance+"\">";
        var colonne1 = "<td>"+etablissement+"</td>";
        var colonne2 = "<td class=\"supp\"><input class=\"bouton_supp\" name=\"retrait\" ";
        colonne2 += "type=\"submit\" value=\"\" id=\""+id_surveillance+"\" </td>";
        var fin_ligne = "</tr>";
        var ligne = nouvelle_ligne + colonne1 + colonne2 + fin_ligne;

        $('.tableau_profil > tbody:last-child').append(ligne);
    }
}

// Cette fonction servira à retirer «visuellement» la ligne qui convient
// l'établissement comme nous avons réussi à la retiré côté serveur.
function supprimer_ligne_tableau_etablissement(id_surveillance){
    var d = document.getElementsByClassName(id_surveillance);
    for (var i = 0; i < d.length; i++) {
        d[i].parentElement.removeChild(d[i]);
    }
}

// Cette fonction sera commune aux appels AJAX avec un code de retour différent de 200 ou 201
function appel_ajax_erreur(section_result, formulaire, section_msg_erreur, msg_erreur){
    section_result.innerHTML = "";
    formulaire.style.border = "2px solid red";
    section_msg_erreur.innerHTML = msg_erreur;
}

// Cette fonction sera pour afficher le résultat des établissements et leur nombre amandes respectifs.
// J'ai découvert comment faire des string avec des variables
// https://stackoverflow.com/questions/19105009/how-to-insert-variables-in-javascript-strings/44510325
function creation_bloc_html_interval(liste){
    // Le bloc HTML pour le résultat de la liste des établissements ave leur nombre de contrevantions
    var result_interval = "<div class=\"tabeau_resto\"><div class=\"ligne\">";
    result_interval += "<div class=\"colonne80\">Établissement</div>";
    result_interval += "<div class=\"colonne20\">Nombre</div></div>";
    for(var i = 0; i < liste.length; i++) {
        result_interval += "<div class=\"ligne\">";
        var resto = liste[i];
        result_interval += `<div class='colonne80'>${resto.etablissement}</div>`;
        result_interval += `<div class='colonne20'>${resto.nombre}</div>`;
        result_interval += "</div>";
    }
    result_interval += "</div>";

    return result_interval;
}

// Utilisation de ce principe pour itérer
// https://zellwk.com/blog/looping-through-js-objects/
function creation_bloc_html_etablissement(listes){
    var result_liste = "";
    for(var i = 0; i < listes.length; i++) {
        result_liste += "<div class=\"tabeau_resto\"><div class=\"ligne\">";
        result_liste += "<div class=\"colonne25\">Type</div>";
        result_liste += "<div class=\"colonne75\">Information</div></div>";
        const une_amande = Object.entries(listes[i]);
        for (const [cle, valeur] of une_amande) {
            result_liste += "<div class=\"ligne\">";
            result_liste += `<div class='colonne25'>${cle}</div>`;
            if (cle == "Montant"){
                result_liste += `<div class='colonne75'>${valeur} $</div>`;
            } else if (cle == "Description"){
                result_liste += `<div class='colonne75 justify'>${valeur}</div>`;
            } else {
                result_liste += `<div class='colonne75'>${valeur}</div>`;
            }
            result_liste += "</div>";
        }
        result_liste += "</div>";
    }

    return result_liste;
}

// Cette fonction sera utiliser pour afficher des informations relatives aux retour des appels AJAX
function creation_bloc_html(listes){
    var result_liste = "";
    result_liste += "<table class=\"tabeau_resto\"><tbody>";
    for (var key in listes) {
        result_liste += "<tr>";
        result_liste += `<td class='plainte_cle'>${key} :</td>`;
        result_liste += `<td class='plainte_valeur'>${listes[key]}</td>`;
        result_liste += "<tr>";
    }
    result_liste += "</tbody></table>";

    return result_liste;
}

// Fonction pour saisir un texte pour le placeholder du Select spécial
function creation_select2(){
    $('.js-example-basic-multiple').select2({
        placeholder: "Choix d'(es) établissement(s)"
    });
}

// Les fonctions ici seront prètes à utiliser au moment que le contenu de la page HTML soit loade rdans son entièter
document.addEventListener('DOMContentLoaded', function () {
    validation_bouton_section_photo();
    recherche();
    recherche_rapide();
    demande_plainte();
    demande_nouveau_profil();
    demande_connection_profil();
    ajout_etablissements_profil();
    retrait_etablissement_profil();
    ajout_modif_retrait_photo_profil();
    reset_recherche();
    reset_recherche_interval();
    reset_demande_plainte();
    reset_nouveau_profil();
    reset_demande_connection();
    reset_gestion_etablissement();
    creation_select2();
});