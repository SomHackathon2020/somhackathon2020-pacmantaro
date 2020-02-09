from flask_login import UserMixin
import json
from __init__ import db

def to_json(inst, cls):
    """
    Jsonify the sql alchemy query result.
    """
    convert = dict()
    # add your coversions for things like datetime's
    # and what-not that aren't serializable.
    d = dict()
    for c in cls.__table__.columns:
        v = getattr(inst, c.name)
        if c.type in convert.keys() and v is not None:
            try:
                d[c.name] = convert[c.type](v)
            except:
                d[c.name] = "Error:  Failed to covert using ", str(convert[c.type])
        elif v is None:
            d[c.name] = str()
        else:
            d[c.name] = v
    return json.dumps(d)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000), unique=True)
    email = db.Column(db.String(1000))
    password = db.Column(db.String(100))

    @property
    def json(self):
        return to_json(self, self.__class__)


class Activitat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    completed = db.Column(db.Boolean)
    titol = db.Column(db.String(1000))
    comentari_adicional = db.Column(db.String(1000))
    descripcio_activitat = db.Column(db.String(1000))
    categoria = db.Column(db.String(1000))
    remuneracio = db.Column(db.Integer) #(integer, si es 0 es voluntat, -1 sera gratis)
    url_imatge = db.Column(db.String(1000))
    rang_persones = db.Column(db.String(1000))
    data = db.Column(db.String(1000))#(datetime amb lloc)
    hora = db.Column(db.String(1000))
    lat = db.Column(db.String(1000))
    lon = db.Column(db.String(1000))
    nom_ubicacio = db.Column(db.String(1000))
    valoracio_mitjana_activitat = db.Column(db.String(1000))
    extra = db.Column(db.String(1000)) #(string)
    keywords = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # , nullable=False))
    user = db.relationship("User", foreign_keys=[user_id])

    @property
    def json(self):
        return to_json(self, self.__class__)