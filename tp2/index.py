# coding: utf8

from flask import Flask
from flask import render_template
from flask import g
from flask import request
from flask import make_response
from flask import redirect
from flask import session
from flask import Response
from flask import jsonify
from flask_cors import CORS, cross_origin
from flask import url_for
from flask_mail import Mail, Message
from database import Database
from functools import wraps
from binascii import a2b_base64
import hashlib
import uuid
import io
import json
import os.path
import datetime
import random


def config_mail():
    config_list = []
    my_path = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(my_path, 'conf.txt')
    with open(path) as c:
        for i in range(2):
            line = c.readline()
            options=line.split(':')
            #remove trailing '\n'
            option=options[1]
            option = option.rstrip()
            #list[0] = mail, list[1] = password
            config_list.append(option)
    return config_list


config_list= config_mail()
mail_default_sender=config_list[0]
mail_username=config_list[0]
mail_password=config_list[1]
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config.update(
    DEBUG=True,
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME=mail_username,
    MAIL_DEFAULT_SENDER=mail_default_sender,
    MAIL_PASSWORD=mail_password
)
mail = Mail(app)


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
        global mail_is_set
        mail_is_set = False


@app.template_filter('b64decode')
def b64decode(value):
    # resp = value.rstrip('\n')
    # resp = str(value)
    # resp ='alo'
    print(value)
    resp = io.StringIO(value['bin'])
    return resp


def authentication_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not is_authenticated(session):
            return send_unauthorized()
        return f(*args, **kwargs)
    return decorated


def is_authenticated(session):
    resp = 'id' in session
    return resp


def send_unauthorized():
    return Response('Could not verify your access level for that URL.\n'
                    'You have to login with proper credentials', 401,
                    {'WWW-Authenticate': 'Basic realm="Login Required"'})


def get_username():
    if 'id' in session:
        return get_db().get_session_username_by_id_session(session['id'])
    return None


@app.route('/')
def start():
    animals = get_db().get_all_animals()
    if 'id' in session:
        return render_template('index.html', animals=animals, id=get_username())
    return render_template('index.html', animals=animals)


@app.route('/search', methods=['POST'])
def get_animals_by_query():
    query = request.json['query']
    option = request.json['option']
    redirect_url = 'http://localhost:5000/search/' + query + '/1'
    return jsonify({'success': True, 'url': redirect_url,})


@app.route('/search/<query>/<int:page>', methods=['GET'])
def get_animals_by_page(query, page):
    data = get_db().get_animals_by_name(query)
    end = page * 5 -1
    start = end - 4
    animals = data[start-1:end-1]

    return render_template('search_results.html', animals=animals, id=get_username(), query=query)


@app.route('/animals/<int:animal_id>', methods=['GET'])
def get_animal_by_id(animal_id):
    animals = get_db().get_animals_by_id(animal_id)
    username = get_username()
    if animals is None:
        return render_template('error.html', erreur='no results'), 404
    else:
        return render_template('search_result_by_id.html', animals=animals, id=username), 200


@app.route('/invite/<token>')
def check_token(token):
    data = get_db().get_account_email_by_token(token)
    if (data is None):
        return render_template('error.html', error='not authorized'), 400
    else:
        return render_template('user_register.html'), 200


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.json['username']
        password = request.json['password']
        if username == '' or password == '':
            error = 'empty username or password'
            return render_template('user_login.html', error=error), 400
        user = get_db().get_user_hash_by_username(username)
        if user is None:
            error = 'incorrect password or username'
            redirect_url = 'http://localhost:5000/login'
            return jsonify({'success': False, 'url': redirect_url, 'error': error})
        salt = user[0]
        hashed_password = hashlib.sha512(str(password + salt).encode('utf-8')).hexdigest()
        if hashed_password == user[1]:
            id_session = uuid.uuid4().hex
            get_db().save_session(id_session, username)
            session['id'] = id_session
            redirect_url = 'http://localhost:5000/myaccount'
            return jsonify({'success': True, 'url': redirect_url})
        else:
            redirect_url = 'http://localhost:5000/login'
            error = 'incorrect password or username'
            return jsonify({'success': False, 'url': redirect_url, 'error':error})
    else:
        return render_template('user_login.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.json['username']
        name = request.json['name']
        family_name = request.json['family_name']
        phone = request.json['phone']
        address = request.json['address']
        password = request.json['password']
        email = request.json['email']
        if username == '' or password == '' or email == '':
            error = 'name, password or email empty'
            return render_template('error.html', error=error), 400
        else:
            salt = uuid.uuid4().hex
            hashed_password = hashlib.sha512(str(password + salt).encode('utf-8')).hexdigest()
            get_db().create_user(username, name, family_name, phone, address, email, salt, hashed_password)
            id_session = uuid.uuid4().hex
            get_db().save_session(id_session, username)
            session['id'] = id_session
            url = 'http://localhost:5000/myaccount'

            return Response(json.dumps({'success': True, 'url': url}), mimetype=u'application/json')

    else:
        return render_template('user_register.html')


@app.route('/logout')
@authentication_required
def logout():
    if 'id' in session:
        id_session = session['id']
        session.pop('id', None)
        get_db().delete_session(id_session)
    return redirect('/')


# @app.route('/')
# def logged_user(username):
#     page = request.args.get('page')
#     animals = get_db().get_all_animals()
#     error = request.args.get('error', None)
#     return render_template('index.html', id=username, animals=animals, error=error)


@app.route('/mypet', methods=['GET','DELETE'])
@authentication_required
def get_mypet():
    if request.method=='GET':
        # TODO add get user id by username
        id = get_db().get_user_id_by_id_session(session['id'])
        animals = get_db().get_animals_by_owner_id(id)
        if animals is None:
            return render_template('error.html', error='no post'), 400
        else:
            return render_template('mypet.html', id=get_username(), animals=animals)
    elif request.method=='DELETE':
        pass


@app.route('/mypet/update', methods=['GET','UPDATE','DELETE'])
@authentication_required
def update_mypet():
    if request.method == 'GET':
        # TODO add get user id by username
        id = get_db().get_user_id_by_id_session(session['id'])
        animals = get_db().get_animals_by_id(id)
        return render_template('mypet_update.html', id=get_username(), animals=animals)
    elif request.method == 'UPDATE':
        # get request data
        name = request.json['name']
        type = request.json['type']
        race = request.json['race']
        age = request.json['age']
        date = datetime.datetime.now().strftime('%Y-%m-%d')
        description = request.json['description']
        img_uri = request.json['img']
        # to prevent colision writing data, prefix the animal owner id since a owner can only post 1 photo
        user_id = get_db().get_user_id_by_id_session(session['id'])
        img_name = name + '_' + str(user_id)
        # front end send data_uri as data:image/base64,XXX
        # where xxx is the blob in string format
        listed_img_uri = img_uri.split(',')
        img_base64_tostring = listed_img_uri[1]
        img_url = ''
        # the photo has been updated
        if len(img_base64_tostring) > 0:
            # convert string to binary data for writing purpose
            binary_data = a2b_base64(img_base64_tostring)
            # allow to run on other machine thus root path is unknown
            my_path = os.path.abspath(os.path.dirname(__file__))
            # TODO add image extention possibilities
            img_url = 'static/img/%s.jpeg' % (img_name,)
            path = os.path.join(my_path, img_url)
            # html will mount relative path
            img_url = '../' + img_url
            # create/save image
            with open(path, 'wb+') as fh:
                fh.write(binary_data)
        get_db().update_animal(name, type, race, age, date, description, img_url, user_id)
        return_url = 'http://localhost:5000/mypet'
        return jsonify({'success': True, 'url': return_url}), 200
    elif request.method == 'DELETE':
        pass


@app.route('/myaccount/update', methods=['GET','UPDATE'])
@authentication_required
def update_myaccount():
    if request.method == 'GET':
        user_infos = get_db().get_user_info_by_username(get_username())
        return render_template('myaccount_update.html', id=get_username(), infos=user_infos)
    elif request.method == 'UPDATE':
        # get request data
        username = request.json['username']
        name = request.json['name']
        family_name = request.json['family_name']
        phone = request.json['phone']
        address = request.json['address']
        password = request.json['password']
        email = get_db().get_user_email_by_username(get_username())

        id=get_db().get_user_id_by_id_session(session['id'])
        salt = uuid.uuid4().hex
        hashed_password = hashlib.sha512(str(password + salt).encode('utf-8')).hexdigest()

        get_db().update_user(id, username, name, family_name, phone, address, email, salt, hashed_password)
        return_url = 'http://localhost:5000/myaccount'
        return jsonify({'success': True, 'url': return_url}), 200


@app.route('/myaccount/', methods=['GET'])
@authentication_required
def get_myaccount():
    user_info = get_db().get_user_info_by_username(get_username())
    if user_info is None:
        return render_template('error.html', error='no post'), 400
    else:
        return render_template('myaccount.html', id=get_username(), infos=user_info)


@app.route('/post', methods=['POST', 'GET'])
@authentication_required
def post():
    if request.method == 'POST':
        # get request data
        name = request.json['name']
        type = request.json['type']
        race = request.json['race']
        age = request.json['age']
        date = datetime.datetime.now().strftime('%Y-%m-%d')
        description = request.json['description']
        img_uri = request.json['img']
        # to prevent colision writing data, we prefix the animal owner id since a owner can only post 1 photo
        user_id = get_db().get_user_id_by_id_session(session['id'])
        if user_has_already_posted:
            username = get_username()
            return_url = 'http://localhost:5000/' + username + '?error=you have already a friend waiting for adoption'
            return jsonify({'success': False, 'url': return_url}), 401
        else:
            save_image_on_disc(user_id=user_id, img_uri=img_uri, name=name)
            img_path=name+'_'+ str(user_id)
            img_url = '../static/img/%s.jpeg' % (img_path,)
            get_db().insert_animal(name, type, race, age, date, description, img_url, user_id)
            return_url = 'http://localhost:5000/mypet'
            return jsonify({'success': True, 'url': return_url}), 200
    else:
        return render_template('user_post.html', id=get_username())


def user_has_already_posted(user_id):
    animals = get_db().get_animals_by_owner_id(user_id)
    if len(animals) > 0:
        return True
    return False


def save_image_on_disc(**kwargs):
    user_id = kwargs['user_id']
    img_uri = kwargs['img_uri']
    name = kwargs['name']
    img_name = name + '_' + str(user_id)
    # front end send data_uri as data:image/base64,XXX
    # where xxx is the blob in string format
    listed_img_uri = img_uri.split(',')
    img_base64_tostring = listed_img_uri[1]
    # convert string to binary data for writing purpose
    binary_data = a2b_base64(img_base64_tostring)
    # allow to run on other machine thus we dont know the root path
    my_path = os.path.abspath(os.path.dirname(__file__))
    # TODO add image extention possibilities
    img_url = 'static/img/%s.jpeg' % (img_name,)
    path = os.path.join(my_path, img_url)
    # create/save image
    with open(path, 'wb+') as fh:
        fh.write(binary_data)


@app.route('/api/add', methods=['POST'])
def api_add():
    data = request.get_json()
    username = data['username']
    password = data['password']
    if username == '' or password == '':
        erreur = 'username ou password  vide'
        return jsonify({'erreur': erreur}), 400
    user = get_db().get_user_hash_by_username(username)
    if user is None:
        error = 'utilisateur inexistant'
        return jsonify({'error': error}), 407
    salt = user[0]
    hashed_password = hashlib.sha512(password + salt).hexdigest()
    if hashed_password != user[1]:
        erreur = 'mot de passe incorrect'
        return jsonify({'erreur': erreur}), 407
    titre = data['titre']
    identifiant = former_identifiant(titre)
    auteur = data['auteur']
    date_publication = data['date_publication']
    paragraphe = data['paragraphe']
    get_db().insert_animal(titre, identifiant, auteur,
                           date_publication, paragraphe)
    return jsonify({'message': 'successfully added '}), 201


@app.route('/api/animal_list', methods=['GET'])
def api_lister_article_publie():
    animals = get_db().get_lastest_animals(1)
    if animals is None:
        return jsonify({'error': 'no animals'}), 204
    return jsonify(animals), 200


@app.route('/api/animal', methods=['POST'])
def information_article():
    data = request.get_json()
    name = data['name']
    animal = get_db().get_animals_by_name(name)
    if animal is None:
        return jsonify({'error': 'not found'}), 404
    id, name, type, race, date_creation, description = animal
    return jsonify({'name': name,
                    'type': type,
                    'race': race,
                    'date_creation': date_creation,
                    'description': description}), 200


@app.route('/password_recovery', methods=['POST','GET'])
def password_recovery():
    if request.method=='POST':
        response = send_recovery_email(request)
        code_status = 200 if response else 400
        return jsonify({'success':response}), code_status
    else:
        return render_template('password_recovery.html')


def send_recovery_email(request):
    user_email = request.json['email']
    token = generate_token(user_email)
    user_infos = get_db().get_user_username_by_email(user_email)
    username = user_infos
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    get_db().save_token(username, user_email, token, date)
    subject = 'recover your password'
    msg = Message(subject, recipients=[user_email])
    msg.body = 'follow this link http://localhost:5000/password_recovery/validate and log with this password: ' + token
    try:
        mail.send(msg)
    except:
        return False
    return True


def generate_token(user_email):
    #generate random number
    list_of_ints = random.sample(range(1, 10), 5)
    new_password = ''.join(str(x) for x in list_of_ints)
    # #update user
    # user_id = get_db().get_user_id_by_email(user_email)
    # salt = uuid.uuid4().hex
    # hashed_password = hashlib.sha512(str(new_password + salt).encode('utf-8')).hexdigest()
    # get_db().update_user_password(user_id, salt, hashed_password)
    return new_password


@app.route('/password_recovery/validate', methods=['POST','GET'])
def password_recovery_validate():
    if request.method=='POST':
        username = request.json['username']
        password = request.json['password']
        token = get_db().get_account_token_by_username(username)
        if token is None:
            error = 'incorrect password or email'
            redirect_url = 'http://localhost:5000/password_recovery/validate'
            return jsonify({'success': False, 'url': redirect_url, 'error': error})
        # salt = token[0]
        # hashed_password = hashlib.sha512(str(password + salt).encode('utf-8')).hexdigest()
        if password == token:
            #update user
            infos = get_db().get_user_info_by_username(username)
            user_id = infos[0]
            salt = uuid.uuid4().hex
            hashed_password = hashlib.sha512(str(token + salt).encode('utf-8')).hexdigest()
            get_db().update_user_password(user_id, salt, hashed_password)
            #update session
            id_session = uuid.uuid4().hex
            get_db().save_session(id_session, username)
            session['id'] = id_session
            redirect_url = 'http://localhost:5000/myaccount'
            return jsonify({'success': True, 'url': redirect_url})
        else:
            redirect_url = 'http://localhost:5000/password_recovery/validate'
            error = 'incorrect password or username'
            return jsonify({'success': False, 'url': redirect_url, 'error': error})
    else:
        return render_template('password_recovery_validate.html')


@app.route('/send_email', methods=['POST'])
def send_email():
    sender_email = request.json['email']
    msg_body = request.json['message']
    animal_id=request.json['animal_id']
    subject = 'someone would like to adopt your little friend ' + sender_email
    recipient=get_db().get_user_email_by_animal_id(animal_id)
    msg = Message(subject, recipients=[recipient])
    msg.body = msg_body
    try:
        mail.send(msg)
    except:
        return jsonify({'success': False, 'error':'Failed to send email, network error'}), 500
    return jsonify({'success': True}), 200


def former_identifiant(titre):
    identifiant = ''
    title = titre.strip()
    for i in range(0, len(title)):
        if title[i].isalpha() or title[i].isspace():
            if title[i].isspace():
                identifiant = identifiant + '_'
            else:
                identifiant = identifiant + title[i]
    identifiant = identifiant.lower()
    data = get_db().get_animals_id_like(identifiant)
    element = '0'
    if len(data) != 0:
        element = data[len(data) - 1]
    if element.isdigit() and element is not '0':
        identifiant = identifiant + int(element) + 1
    return identifiant


app.secret_key = '(*&*&322387he738220)(*(*22347657'

if __name__ == '__main__':
    app.run()
