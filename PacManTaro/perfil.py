from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import csv

from models import User, Activitat

from __init__ import db

perfil = Blueprint('perfil', __name__)

"""
@login_required
@perfil.route('/perfil')
def profile():
    if current_user.is_authenticated:
        my_activities = Activitat.query.filter_by(user_id=current_user.id)
        return render_template('profile.html', activities=my_activities, actiu=True)
    return render_template('login.html')
"""
"""
@login_required
@perfil.route('/perfil/<int:id_activitat>')
def inscriume(id_activitat):
    if current_user.is_authenticated:
        this_activities = Activitat.query.filter_by(id=id_activitat)
        this_activities.inscrits = this_activities.inscrits + ", "
        return render_template('profile.html', activities=this_activities, actiu=True)
    return render_template('login.html')
"""

@perfil.route('/perfil')
def perfil_personal():
    if current_user.is_authenticated:
        this_activities = Activitat.query.filter_by(user_id=current_user.id)
        #this_activities.inscrits = this_activities.inscrits + ", "
        return render_template('profile_own.html', activities=this_activities, actiu=True)
    return render_template('login.html')


@perfil.route('/inscripcions')
def perfil_inscripcions():
    if current_user.is_authenticated:
        this_activities = Activitat.query.all()
        wanted_id = current_user.id
        acts_inscrits = []
        for el in this_activities:
            if str(wanted_id) in el.inscrits:
                acts_inscrits.append(el)



        #this_activities.inscrits = this_activities.inscrits + ", "
        return render_template('profile_own.html', activities=acts_inscrits, actiu=True, hideContact=True)
    return render_template('login.html')

@perfil.route('/inscriume/<int:id_activitat>')
def inscriume(id_activitat):
    if current_user.is_authenticated:
        this_activity = Activitat.query.filter_by(id=id_activitat).first()
        this_activity.inscrits = this_activity.inscrits + ", " + str(current_user.id)
        db.session.add(this_activity)
        db.session.commit()
        #this_activities.inscrits = this_activities.inscrits + ", "
        return render_template('activity_detail_own.html', this_activity=this_activity, actiu=True)
    else:
        return render_template('login.html')