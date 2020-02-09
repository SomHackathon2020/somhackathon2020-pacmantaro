from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

import pandas as pd
import pandas
import folium
import os
import json
import tempfile
import time



from models import User, Activitat

from __init__ import db

pdf_form = Blueprint('pdf_form', __name__)


@pdf_form.route('/form_test/<int:id_activitat>')
def form_test(id_activitat):
    print(id_activitat)

    return render_template('activity_base.html')