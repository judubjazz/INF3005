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

from flask import Flask, render_template, g, request, redirect, session, url_for, Response, make_response, jsonify
from database import Database
import re
import datetime


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


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/')
def start_page():
    return render_template('accueil.html')


@app.route('/<matricule>/')
def matricule(matricule):
    if not valid_format_matricule(matricule):
        return render_template('accueil.html', erreur="mauvais format de matricule"),400


    info = get_db().get_matricule_info(matricule)
    if info is None:
        return render_template("404.html", erreur="il n'y a pas de matricule à ce nom"), 404
    dates = get_db().get_matricule_dates(matricule)
    mois = get_mois(dates)
    return render_template('mois.html', matricule=matricule, mois=mois)


@app.route('/<matricule>/<date_du_jour>')
def date_du_jour(matricule, date_du_jour):
    if not valid_format_matricule(matricule):
        return render_template('accueil.html', erreur="mauvais format de matricule"),400
    if not valid_format_date(date_du_jour):
        return render_template('accueil.html', erreur="mauvais format de date"),400

    info = get_db().get_matricule_info(matricule)
    if info is None:
        return render_template("404.html", erreur="il n'y a pas de matricule à ce nom"), 404

    info = get_db().get_date_du_jour_info(matricule, date_du_jour)
    if not info:
        return render_template('jour.html', date=date_du_jour, erreur='il n y a pas de donné pour ce jour')
    return render_template('jour.html', matricule=matricule, infos=info, date=date_du_jour, mois=None)


@app.route('/<matricule>/overview/<mois>')
def overview(matricule, mois):
    if not valid_format_matricule(matricule):
        return render_template('accueil.html', erreur="mauvais format de matricule")
    if not verifier_format_mois(mois):
        return render_template('mois.html', erreur="mauvais format mois")

    info = get_db().get_matricule_info(matricule)
    if info is None:
        return render_template("404.html", erreur="il n'y a pas de matricule à ce nom"), 404

    infos = get_db().get_mois_info(matricule, mois)
    return render_template('overview.html', infos=infos)


@app.route('/login', methods=['POST', 'UPDATE', 'DELETE'])
def log_user():
    if request.method == 'POST':
        matricule = request.form["matricule"]
        if matricule == "":
            return redirect("/")
        now = datetime.datetime.now()
        date_jour = str(now)[:10]
        return redirect(url_for('date_du_jour', matricule=request.form["matricule"], date_du_jour=date_jour))

    elif request.method == 'DELETE':
        get_db().delete_id(request.json['id'])
        reponse = jsonify(request.json)
        return reponse

    elif request.method == 'UPDATE':
        get_db().update_id(request.json)
        response = jsonify(request.json)
        return response


def verifier_format_mois(mois):
    return re.match(r'^\d{4}-\d\d$', mois)


def valid_format_date(date_du_jour):
    try:
        datetime.datetime.strptime(date_du_jour, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def get_mois(dates):
    mois = set()
    for date in dates:
        mois.add(date[0:-3])
    return mois


def valid_format_matricule(matricule):
    return re.match(r'^[A-Z]{3}-[0-9]{2}$', matricule)


if __name__ == '__main__':
    app.run()