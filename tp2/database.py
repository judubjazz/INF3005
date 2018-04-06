# coding: utf8

# Copyright 2017 Jacques Berger
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import sqlite3


class Database:
    def __init__(self):
        self.connection = None

    def get_connection(self):
        if self.connection is None:
            self.connection = sqlite3.connect('/home/ju/JetBrainsProjects/PycharmProjects/webII_tp2/db/database.db')
        return self.connection

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()

    def get_lastest_animals(self, option):
        connexion = self.get_connection()
        cursor = connexion.cursor()
        cursor.execute(" SELECT * FROM Animal WHERE "
                       "strftime('%Y-%m-%d','now') >= strftime"
                       "('%Y-%m-%d',date_creation) ORDER BY "
                       "date_creation DESC")
        if option == 1:
            return self.animal_to_list_of_dict(cursor.fetchall())
        else:
            return cursor.fetchmany(5)

    def get_animals_by_name(self, query):
        connexion = self.get_connection()
        cursor = connexion.cursor()
        sql_query = "%" + query + "%"
        cursor.execute(("SELECT * FROM Animal WHERE name LIKE ? OR "
                        "Animal.description LIKE ? AND "
                        "strftime('%Y-%m-%d','now') >= strftime"
                        "('%Y-%m-%d', date_creation)"), (sql_query, sql_query,))
        return cursor.fetchall()

    def get_all_animals(self):
        connexion = self.get_connection()
        cursor = connexion.cursor()
        cursor.execute('SELECT * FROM Animal')
        return cursor.fetchall()

    def get_animal_by_name(self, name):
        connexion = self.get_connection()
        cursor = connexion.cursor()
        sql_query = "%" + name + "%"
        cursor.execute("SELECT * FROM Animal WHERE name LIKE ?", (sql_query,))
        return cursor.fetchone()

    def get_animals_by_id(self, id):
        connexion = self.get_connection()
        cursor = connexion.cursor()
        cursor.execute("SELECT * FROM Animal WHERE id = ?", (id,))
        return cursor.fetchall()

    def get_animals_by_owner_id(self, owner_id):
        connexion = self.get_connection()
        cursor = connexion.cursor()
        cursor.execute("SELECT * FROM Animal WHERE id = ?", (owner_id,))
        return cursor.fetchall()

    def get_animals_id_like(self, id):
        connexion = self.get_connection()
        cursor = connexion.cursor()
        sql_id = "%" + id + "%"
        cursor.execute("SELECT * FROM Animal WHERE id LIKE ?",
                       (sql_id,))
        return cursor.fetchall()

    def update_animal(self, name, type, race, age, date_creation, description, img_url, owner_id):
        connexion = self.get_connection()
        cursor = connexion.cursor()
        if img_url == '':
            # no need to update image
            sql_query = 'UPDATE Animal SET name=?, type=?, race=?, age=?, date_creation=?, description=? WHERE owner_id=?'
            cursor.execute(sql_query, (name, type, race, age, date_creation, description, owner_id,))
        else:
            sql_query = 'UPDATE Animal SET name=?, type=?, race=?, age=?, date_creation=?, description=?, img_url=? WHERE owner_id=?'
            cursor.execute(sql_query, (name, type, race, age, date_creation, description, img_url, owner_id,))
        connexion.commit()
        return cursor.fetchone()

    def insert_animal(self, name, type, race, age, date_creation, description, img_url, owner_id):
        connexion = self.get_connection()
        cursor = connexion.cursor()
        cursor.execute("INSERT INTO Animal(name, type, race, age, date_creation, description, img_url, owner_id) "
                       "VALUES(?, ?, ?, ?, ?,?,?, ?)",
                       (name, type, race, age, date_creation, description, img_url, owner_id,))
        connexion.commit()

    def create_user(self, username, name, family_name, phone, address, email, salt, hashed_password):
        connection = self.get_connection()
        connection.execute(("INSERT INTO Users(username, name, family_name, phone, address, email, salt, hash)"
                            " VALUES(?, ?, ?, ?, ?, ?, ?, ?)"), (username, name, family_name, phone, address, email, salt,
                                                        hashed_password))
        connection.commit()

    def get_user_id_by_email(self,email):
        cursor = self.get_connection().cursor()
        cursor.execute('SELECT id FROM Users WHERE username=?', (email,))
        user = cursor.fetchone()
        if user is None:
            return None
        else:
            return user[0]

    def get_user_hash_by_username(self, username):
        cursor = self.get_connection().cursor()
        cursor.execute('SELECT salt, hash FROM Users WHERE username=?', (username,))
        user = cursor.fetchone()
        if user is None:
            return None
        else:
            return user[0], user[1]

    def get_user_info_by_username(self, username):
        cursor = self.get_connection().cursor()
        cursor.execute('SELECT * FROM Users WHERE username=?', (username,))
        user = cursor.fetchone()
        if user is None:
            return None
        else:
            return user[0], user[1], user[2], user[3], user[4], user[5]

    def get_user_username_by_email(self, email):
        cursor = self.get_connection().cursor()
        cursor.execute('SELECT username FROM Users WHERE email=?', (email,))
        user = cursor.fetchone()
        if user is None:
            return None
        else:
            return user[0]

    def get_user_email_by_animal_id(self, animal_id):
        cursor = self.get_connection().cursor()
        cursor.execute('SELECT email FROM Users u JOIN Animal a ON u.id = a.owner_id WHERE a.id=?', (animal_id,))
        email = cursor.fetchone()
        return email[0]

    def get_user_email_by_username(self, username):
        cursor = self.get_connection().cursor()
        cursor.execute('SELECT email FROM Users u WHERE u.username=?', (username,))
        email = cursor.fetchone()
        return email[0]

    def get_user_id_by_id_session(self, id_session):
        cursor = self.get_connection().cursor()
        cursor.execute('SELECT DISTINCT  u.id '
                       'FROM sessions s JOIN Users u '
                       'ON s.username = u.name '
                       'WHERE id_session=?', (id_session,))
        data = cursor.fetchone()
        if data is None:
            return None
        else:
            return data[0]

    def get_all_users(self):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM Users')
        return cursor.fetchall()

    def update_user_password(self,id, salt, hash):
        connection = self.get_connection()
        connection.execute('UPDATE Users SET salt=?, hash=? WHERE id=?',(salt, hash, id,))
        connection.commit()

    def update_user(self,id, username, name, family_name, phone, address, email, salt, hash):
        connection = self.get_connection()
        connection.execute('UPDATE Users '
                           'SET username=?, name=?, family_name=?, phone=?, address=?, email=?, salt=?, hash=? '
                           'WHERE id=?',(username, name, family_name, phone, address, email, salt, hash, id,))
        connection.commit()

    def save_session(self, id_session, username):
        connection = self.get_connection()
        connection.execute(("INSERT INTO sessions(id_session, username) "
                            "VALUES(?, ?)"), (id_session, username,))
        connection.commit()

    def delete_session(self, id_session):
        connection = self.get_connection()
        connection.execute("DELETE FROM sessions WHERE id_session=?",
                           (id_session,))
        connection.commit()

    def get_session_username_by_id_session(self, id_session):
        cursor = self.get_connection().cursor()
        cursor.execute("SELECT username FROM sessions WHERE id_session=?",
                       (id_session,))
        data = cursor.fetchone()
        if data is None:
            return None
        else:
            return data[0]

    def get_account_token_by_username(self, username):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT token FROM Account WHERE username=?",
                       (username,))
        data = cursor.fetchone()
        if data is None:
            return None
        else:
            cursor.execute("DELETE FROM Account WHERE username=?", (username,))
            connection.commit()
            return data[0]

    def animal_to_list_of_dict(self, animal):
        list_animal = []
        for row in animal:
            list_animal.append(self.to_dict(row))
        return list_animal

    def save_token(self, username , user_email, token , date):
        connection = self.get_connection()
        connection.execute("INSERT INTO Account(username, email,token,date_sent) "
                           "VALUES(?, ?, ?, ?)",
                           (username, user_email, token, date))
        connection.commit()

    def to_dict(self, row):
        return {"id": row[0], "titre": row[1], "identifiant": row[2],
                "auteur": row[3], "date_publication": row[4],
                "paragraphe": row[5]}
