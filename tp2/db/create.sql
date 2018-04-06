create table Users (
  id integer primary key,
  username varchar(32) UNIQUE,
  name varchar(32),
  family_name varchar(32),
  phone varchar(32),
  address varchar(128),
  email varchar(32) UNIQUE,
  salt varchar(32),
  hash varchar(128)
);

create table Animal (
  id integer primary key,
  name varchar(64),
  type varchar(32),
  race varchar(32),
  age integer,
  date_creation date,
  description varchar(512),
  img_url varchar(128),
  owner_id integer,
  FOREIGN KEY (owner_id) REFERENCES Users(id)
  ON DELETE NO ACTION
  ON UPDATE CASCADE
);

create table sessions (
  id integer primary key,
  id_session varchar(32),
  username varchar(32)
);

create table Account (
  id integer primary key,
  username varchar(32) UNIQUE,
  email varchar(32) UNIQUE,
  token varchar(32),
  date_sent text
);


INSERT INTO Animal (id, name, type, race, age, date_creation, description, img_url, owner_id) VALUES (1,'bearette','bear','bearus',5,'2018-03-05','beautiful polar bear','../static/img/bear.jpeg',1);
INSERT INTO Animal (id, name, type, race, age, date_creation, description, img_url, owner_id) VALUES (2,'squirette','rat','squirus',5,'2018-03-05','beautiful squirel','../static/img/squirel.jpeg',2);
INSERT INTO Animal (id, name, type, race, age, date_creation, description, img_url, owner_id) VALUES (3,'pandette','panda','pandus',5,'2018-03-05','beautiful panda','../static/img/panda.jpeg',3);
INSERT INTO Animal (id, name, type, race, age, date_creation, description, img_url, owner_id) VALUES (4,'zebrette','horse','zebrus',5,'2018-03-05','beautiful zebra','../static/img/zebra.jpeg',4);
INSERT INTO Animal (id, name, type, race, age, date_creation, description, img_url, owner_id) VALUES (5,'elephette','elephant','elephus',5,'2018-03-05','beautiful elephant','../static/img/elephant.jpeg',5);

SELECT * FROM Animal;