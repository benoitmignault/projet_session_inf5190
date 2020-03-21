create table mauvais_restaurants (
	id_resto integer primary key AUTOINCREMENT,
	proprietaire varchar(100) not null,
	categorie varchar(50) not null,
	etablissement varchar(65) not null,
	adresse varchar(35) not null,
	ville varchar(40) not null,
	description varchar(800) not null,
	date_infraction varchar(10) not null,
	date_jugement varchar(10) not null,
	montant_amende integer not null
);