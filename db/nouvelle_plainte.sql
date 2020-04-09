create table departement_plaintes (
	id_plainte integer primary key AUTOINCREMENT,	
	etablissement varchar(65) not null,
	no_civique varchar(10) not null,
	nom_rue varchar(35) not null,
	ville varchar(40) not null,	
	date_visite varchar(10) not null,
	prenom_plaignant varchar(35) not null,
	nom_plaignant varchar(35) not null,
	description varchar(800) not null
);
