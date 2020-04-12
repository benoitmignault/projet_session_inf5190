create table profil_utilisateur (
	id_personne integer primary key AUTOINCREMENT,
	id_photo integer unique not null,
	nom varchar(50) not null,
  prenom varchar(50) not null,
  password varchar(100) not null,
	courriel varchar(50) not null
);
