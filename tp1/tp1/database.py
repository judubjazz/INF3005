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
            self.connection = sqlite3.connect('db/database.db')
        return self.connection


    def disconnect(self):
        if self.connection is not None:
            self.connection.close()


    def create_matricule(self, matricule, code_de_projet, date_publication, duree):
        connection = self.get_connection()
        connection.execute(("insert into heures(matricule, code_de_projet, date_publication, duree)"
                            " values(?, ?, ?, ?)"), (matricule, code_de_projet, date_publication,
                                                     duree))
        connection.commit()


    def get_matricule_info(self, matricule):
        cursor = self.get_connection().cursor()
        cursor.execute(("select * from heures where matricule=?"),
                       (matricule,))
        matricule = cursor.fetchone()
        if matricule is None:
            return None
        else:
            return matricule[0], matricule[1]


    def get_matricule_dates(self, matricule):
        cursor = self.get_connection().cursor()
        cursor.execute(("select date_publication from heures where matricule=?"),
                       (matricule,))
        dates = cursor.fetchall()
        if dates is None:
            return None
        else:
            return [date[0] for date in dates]


    def get_date_du_jour_info(self, matricule, date_du_jour):
        cursor = self.get_connection().cursor()
        cursor.execute(("select * from heures where matricule=? AND date_publication=?"),
                       (matricule,date_du_jour))
        infos = cursor.fetchall()
        if infos is None:
            return None
        else:
            return [(info[0], info[1], info[2], info[3], info[4]) for info in infos]


    def get_mois_info(self, matricule, date_du_jour):
        date_debut= date_du_jour+"-00"
        date_fin= date_du_jour+"-31"
        cursor = self.get_connection().cursor()
        cursor.execute(("select * from heures where matricule=? AND date_publication BETWEEN ? and ?"),
                       (matricule,date_debut, date_fin))
        infos = cursor.fetchall()
        if infos is None:
            return None
        else:
            return [(info[0], info[1], info[2], info[3], info[4]) for info in infos]


    def delete_id(self,id):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(("delete from heures where id=? "),(id,))
        connection.commit()


    def update_id(self,request_json):
        id = request_json['id']
        duree = request_json['duree']
        date_publication = request_json['date_publication']
        code_projet = request_json['code_projet']
        matricule = request_json['matricule']

        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(("update heures set matricule=?, code_de_projet=?, date_publication =?, duree = ?  where id=? "),(matricule,code_projet,date_publication, duree, id,))
        connection.commit()
