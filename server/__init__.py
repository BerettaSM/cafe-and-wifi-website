from os import path
from secrets import token_hex

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
DB_NAME = 'cafes.db'


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = token_hex(32)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    create_database(app)

    from .views import views
    app.register_blueprint(views, url_prefix='/')

    return app


def create_database(app):
    if not path.exists(path.join('instance', DB_NAME)):
        with app.app_context():
            db.create_all()
        print('Database created!')
