create table profil_utilisateur (
	id_personne integer primary key AUTOINCREMENT,
	id_photo integer unique,
	nom varchar(50) not null,
	type_photo varchar(3),
  prenom varchar(50) not null,
	salt varchar(32) not null,
	hash varchar(128) not null,
	courriel varchar(50) unique not null
);
