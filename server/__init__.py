from os import path
from secrets import token_hex

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from .utils import insert_dummy_data


db = SQLAlchemy()
DB_NAME = 'cafes.db'


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = token_hex(32)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .models import Cafe, User
    create_database(app)

    from .views import views
    app.register_blueprint(views, url_prefix='/')

    from .auth import auth
    app.register_blueprint(auth, url_prefix='/')

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    return app


def create_database(app):
    if not path.exists(path.join('instance', DB_NAME)):
        with app.app_context():
            db.create_all()
            insert_dummy_data(db)
        print('Database created!')
