create table heures (
  id integer primary key,
  matricule varchar(6),
  code_de_projet varchar(15),
  date_publication text,
  duree integer
);
insert into heures values (1, 'AAA-12', "1234", "2000-01-01",1);
insert into heures values (2, 'AAA-12', "1234", "2000-02-01",1);

select * from heures where matricule="AAA-12" AND date_publication="2000-01-01";