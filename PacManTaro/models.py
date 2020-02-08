from flask_login import UserMixin
from __init__ import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    email = db.Column(db.String(1000))
    password = db.Column(db.String(100))


class Activitat(db.Model):
    id = db.Column(db.Integer, primary_key=True)