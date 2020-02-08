from flask_login import UserMixin
from __init__ import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    email = db.Column(db.String(1000))
    password = db.Column(db.String(100))


class Activitat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titol = db.Column(db.String(1000))
    persona = db.Column(db.String(1000))
    comentari_adicional = db.Column(db.String(1000))
    descripcio_activitat = db.Column(db.String(1000))
    categoria = db.Column(db.String(1000))
    remuneracio = db.Column(db.Integer) #(integer, si es 0 es voluntat, -1 sera gratis)
    url_imatge = db.Column(db.String(1000))
    rangpersones = db.Column(db.String(1000))
    data = db.Column(db.String(1000))#(datetime amb lloc)
    hora = db.Column(db.String(1000))
    lat = db.Column(db.String(1000))
    lon = db.Column(db.String(1000))
    nom_ubicacio = db.Column(db.String(1000))
    valoraciomitjanaactivitat = db.Column(db.String(1000))
    extra = db.Column(db.String(1000)) #(string)
    keywords = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # , nullable=False))
    user = db.relationship("User", foreign_keys=[user_id])