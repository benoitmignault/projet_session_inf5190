create table profil_utilisateur (
	id_personne integer primary key AUTOINCREMENT,
	id_photo integer unique not null,
	nom varchar(50) not null,
  prenom varchar(50) not null,
  password varchar(128) not null,
	salt varchar(32) not null,
	courriel varchar(50) unique not null
);
