from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import csv

from models import User, Activitat

from __init__ import db

analysis = Blueprint('analysis', __name__)

@analysis.route('/testanalysis')
def testanalysis():
    return "<b>Works!</b>"