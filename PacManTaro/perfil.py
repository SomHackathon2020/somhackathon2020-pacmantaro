from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import csv

from models import User, Activitat

from __init__ import db

perfil = Blueprint('perfil', __name__)


@login_required
@perfil.route('/perfil')
def profile():
    if current_user.is_authenticated:
        my_activities = Activitat.query.filter_by(user_id=current_user.id)
        return render_template('profile.html', activities=my_activities, actiu=True)
    return render_template('login.html')