from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import csv

from models import User, Activitat

from __init__ import db

analysis = Blueprint('analysis', __name__)

@analysis.route('/user_acts/<user_id>', methods=['GET'])
def user_acts(user_id):
	acts = Activitat.query.filter_by(user_id=user_id)
	acts = acts if acts else []
	return render_template("act_list.html", acts = acts)


@analysis.route('/act/<ide>', methods=['GET'])
def act(ide):
	acts = Activitat.query.filter_by(id=ide)
	acts = acts if acts else []
	return render_template("act_list.html", acts = acts)


@analysis.route('/test/<ide>', methods=['GET'])
def testing(ide):
	acts = Activitat.query.filter_by(id=ide)
	acts = acts if acts else []
	return render_template("act_list.html", acts = acts)