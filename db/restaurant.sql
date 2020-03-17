create table mauvais_restaurants (
	id_resto integer primary key AUTOINCREMENT,
	proprietaire varchar(25) not null,
	categorie varchar(25) not null,
	etablissement varchar(25) not null,
	adressse varchar(50) not null,
	nom_ville varchar(50) not null,
	description varchar(1000) not null,
	date_infraction varchar(10) not null,
	date_jugement varchar(10) not null,
	montant_amende integer not null
);