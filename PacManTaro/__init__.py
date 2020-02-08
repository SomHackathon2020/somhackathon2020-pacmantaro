from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# custom adds for unsplash api
#from img_api_utils import *

db = SQLAlchemy()
app = Flask(__name__)

app.config['SECRET_KEY'] = 'random-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'main.login'
login_manager.init_app(app)


from models import User


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


from main import main as main_blueprint
app.register_blueprint(main_blueprint)


from activity import activity as activity_blueprint
app.register_blueprint(activity_blueprint)


from analysis import analysis as analysis_blueprint
app.register_blueprint(analysis_blueprint)


def create_app():
    return app
