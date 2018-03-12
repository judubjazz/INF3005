create table heures (
  id integer primary key,
  matricule varchar(6),
  code_de_projet varchar(15),
  date_publication text,
  duree integer
);


insert into heures values (1, 'AAA-12', "1234", "2018-01-01",1);
insert into heures values (2, 'AAA-12', "1234", "2018-01-01",1);
insert into heures values (3, 'AAA-12', "1234", "2018-02-01",1);
insert into heures values (4, 'AAA-12', "1234", "2018-02-02",1);
insert into heures values (5, 'AAA-12', "1234", "2018-02-14",1);
insert into heures values (6, 'AAA-12', "1234", "2018-02-15",1);
insert into heures values (7, 'AAA-12', "1234", "2018-02-16",1);
insert into heures values (8, 'AAA-12', "1234", "2018-02-17",1);
insert into heures values (9, 'BBB-12', "1234", "2018-01-01",1);
insert into heures values (10, 'BBB-12', "1234", "2018-01-01",1);
insert into heures values (11, 'BBB-12', "1234", "2018-02-01",1);
insert into heures values (12, 'BBB-12', "1234", "2018-02-02",1);

insert into heures values (13, 'AAA-12', "1234", "2018-01-01",1);
insert into heures values (14, 'AAA-12', "1234", "2018-01-01",1);
insert into heures values (15, 'AAA-12', "1234", "2018-01-01",1);
insert into heures values (16, 'AAA-12', "1234", "2018-01-01",1);

select * from heures where matricule="AAA-12" AND date_publication="2018-01-01";
select * from heures where matricule="AAA-12" AND date_publication BETWEEN "2018-01-00" AND "2018-01-31";
select * from heures where matricule="AAA-12" AND date_publication BETWEEN "2018-02-00" AND "2018-02-31";