create table etablissement_surveiller (
  id_surveillance integer primary key AUTOINCREMENT,
	id_personne integer not null,
	etablissement varchar(65) not null
);