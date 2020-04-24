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

create table mauvais_restaurants_modif (
	id_resto integer primary key,
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

create table mauvais_restaurants_supp (
	id_resto integer primary key,
  etablissement varchar(65) not null
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
	id_photo varchar(32) unique,
	nom varchar(50) not null,
	type_photo varchar(3),
  prenom varchar(50) not null,
	salt varchar(32) not null,
	hash varchar(128) not null,
	courriel varchar(50) unique not null
);

create table session_profil (
  id integer primary key AUTOINCREMENT,
  id_session varchar(32) unique not null,
  courriel varchar(50) not null
);

CREATE TABLE photo_utilisateur (
	id_photo varchar(32) primary key,
	photo blob
);

create table etablissement_surveiller (
  id_surveillance integer primary key AUTOINCREMENT,
	id_personne integer not null,
	etablissement varchar(65) not null,
  lien_desabonnement	varchar (128) unique,
  UNIQUE(id_personne, etablissement)
);