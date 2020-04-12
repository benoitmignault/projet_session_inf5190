create table mauvais_restaurants (
	id_resto integer primary key AUTOINCREMENT,
	proprietaire varchar(100) not null,
	categorie varchar(50) not null,
	etablissement varchar(65) not null,
	no_civique varchar(10) not null,
	nom_rue varchar(35) not null,
	ville varchar(40) not null,
	description varchar(800) not null,
	date_infraction varchar(10) not null,
	date_jugement varchar(10) not null,
	montant_amende integer not null
);

create table departement_plaintes (
	id_plainte integer primary key AUTOINCREMENT,	
	etablissement varchar(65) not null,
	no_civique integer not null,
	nom_rue varchar(35) not null,
	ville varchar(40) not null,	
	date_visite varchar(10) not null,
	prenom_plaignant varchar(35) not null,
	nom_plaignant varchar(35) not null,
	description varchar(800) not null
);

create table profil_utilisateur (
	id_personne integer primary key AUTOINCREMENT,
	id_photo integer unique,
	nom varchar(50) not null,
  	prenom varchar(50) not null,
  	password varchar(128) not null,
	salt varchar(32) not null,
	courriel varchar(50) unique not null
);

create table etablissement_surveiller (
    id_surveillance integer primary key AUTOINCREMENT,
	id_personne integer not null,
	etablissement varchar(65) not null,
    UNIQUE(id_personne, etablissement)
);

create table photo_utilisateur (
    id_photo integer primary key AUTOINCREMENT,
	photo blob not null
);
