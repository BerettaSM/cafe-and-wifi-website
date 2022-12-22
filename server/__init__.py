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

    from .models import Cafe
    create_database(app)

    from .views import views
    app.register_blueprint(views, url_prefix='/')

    from .auth import auth
    app.register_blueprint(auth, url_prefix='/')

    return app


def create_database(app):
    if not path.exists(path.join('instance', DB_NAME)):
        with app.app_context():
            db.create_all()
            insert_dummy_data()
        print('Database created!')


def insert_dummy_data():
    import csv
    from .models import Cafe
    with open('entries.csv', encoding='UTF-8', newline='') as file:
        reader = csv.DictReader(file)
        dummy_entries = [
            Cafe(
                name=row['name'],
                map_url=row['map_url'],
                img_url=row['img_url'],
                location=row['location'],
                has_sockets=row['has_sockets'] == 'True',
                has_toilet=row['has_toilet'] == 'True',
                has_wifi=row['has_wifi'] == 'True',
                can_take_calls=row['can_take_calls'] == 'True',
                seats=row['seats'],
                coffee_price=row['coffee_price']
            )
            for row in reader
        ]
    db.session.bulk_save_objects(dummy_entries)
    db.session.commit()
