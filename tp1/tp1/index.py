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

from flask import Flask
from flask import render_template
from flask import g
from flask import request
from flask import redirect
from flask import session
from flask import Response
from flask import url_for
from database import Database
import re
import datetime
import string
import hashlib
import uuid
from functools import wraps

app = Flask(__name__)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = Database()
    return g._database


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.disconnect()


@app.route('/')
def start_page():
    return render_template('accueil.html')


@app.route('/erreur')
def erreur():
    return render_template('accueil.html', erreur="mauvais format de matricule")


@app.route('/<matricule>/')
def matricule(matricule):
    if not valid_format_matricule(matricule):
        return render_template('accueil.html', erreur="mauvais format de matricule")

    info = get_db().get_matricule_info(matricule)
    if info is None:
        return render_template("accueil.html", error="il n'y a pas de matricule a ce nom")
    dates = get_db().get_matricule_dates(matricule)
    mois = get_mois(dates)
    return render_template('mois.html', matricule=matricule, mois=mois)


@app.route('/<matricule>/<date_du_jour>')
def date_jour(matricule, date_du_jour):
    if not valid_format_date(date_du_jour):
        return render_template('accueil.html', erreur = "mauvais format de date")
    info = get_db().get_date_du_jour_info(matricule, date_du_jour)
    return render_template('mois.html', matricule=matricule, infos=info, date=date_du_jour, mois=None)


@app.route('/<matricule>/overview/<mois>')
def overview(matricule, mois):
    if not verifier_format_mois(mois):
        return render_template('mois.html', erreur="mauvais format mois")
    db = get_db()
    dates = db.get_matricule_dates(matricule)
    mois= get_mois(dates)
    return render_template('overview.html')


@app.route('/login', methods=["POST"])
def log_user():
    matricule = request.form["matricule"]

    # Vérifier que les champs ne sont pas vides
    if matricule == "":
        return redirect("/")

    return redirect(url_for('matricule', matricule=request.form["matricule"]))


def verifier_format_mois(mois):
    return re.match(r'^\d{4}-\d\d$', mois)


def valid_format_date(date_du_jour):
    try:
        datetime.datetime.strptime(date_du_jour, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def get_mois(dates):
    mois=list()
    for date in dates:
        mois.append(date[0:-3])
    return mois

def valid_format_matricule(matricule):
    return re.match(r'^[A-Z]{3}-[0-9]{2}$', matricule)


if __name__ == '__main__':
    app.run()