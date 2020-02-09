from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import csv

from models import User

from __init__ import db

main = Blueprint('main', __name__)


class Commercial():
    def __init__(self, codiaccess, adreca, epigrafiae, epigrafdesc, latitude, longitude, wkt):
        self.codiaccess = codiaccess,
        self.adreca = adreca,
        self.epigrafiae = epigrafiae,
        self.epigrafdesc = epigrafdesc,
        self.latitude = latitude
        self.longitude = longitude
        self.wkt = wkt

    def __str__(self):
        return str(self.latitude) + ", " \
               + str(self.longitude) + ", " \
               + str(self.codiaccess) + ", " \
               + str(self.adreca)


@main.route('/index')
def index():
    return render_template('index.html')


@main.route('/projects')
def projects():
    return "Projects"


@main.route('/about')
def about():
    return "About"


@main.route('/show')
def show():
    all_users = User.query.all()
    return render_template('show.html', all_users=all_users)


@main.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('activity.search_activity'))
    return render_template('login.html')


@main.route('/login_base')
def login_base():
    return render_template('login_base.html')


@main.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('Comprovi les credencials i torni-ho a intentar.')
        return redirect(url_for('main.login'))

    login_user(user, remember=remember)
    return redirect(url_for('activity.search_activity'))


@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Sessió tancada correctament")
    return redirect(url_for('main.login'))


@main.route('/signup')
def signup():
    return render_template('signup.html')


@main.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if user:
        flash('Adreça ja registrada')
        return redirect(url_for('main.signup'))

    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('activity.search_activity'))


@main.route('/maps')
def maps():
    """ VALUES TO EDIT: """

    name_to_open_file = "act_comercial.csv"

    """ END OF VALUES TO EDIT """

    full_path_to_open_file = "static/databases/" + name_to_open_file

    with open(full_path_to_open_file) as csv_file:
        reader = csv.DictReader(csv_file)
        all_commercial_list = []
        for row in reader:
            if row["LAT"] and row["LNG"] and row["CODI_ACCES"]:
                new_commercial = Commercial(row['CODI_ACCES'], row['ADRECA'], row['EPIGRAF_IAE'], row['EPIGRAF_DESC'], row['LAT'], row['LNG'], row['WKT'])
                all_commercial_list.append(new_commercial)
                print(new_commercial)
        return render_template('leaflet_map.html', records=all_commercial_list)
