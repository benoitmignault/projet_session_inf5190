create table session_profil (
  id integer primary key AUTOINCREMENT,
  id_session varchar(32) unique not null,
  courriel varchar(50) not null
);