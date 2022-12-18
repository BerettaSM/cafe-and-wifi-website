from . import db


class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    map_url = db.Column(db.String(1000), unique=True, nullable=False)
    img_url = db.Column(db.String(1000), unique=True, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    has_sockets = db.Column(db.Boolean, default=False)
    has_toilet = db.Column(db.Boolean, default=False)
    has_wifi = db.Column(db.Boolean, default=False)
    can_take_calls = db.Column(db.Boolean, default=False)
    seats = db.Column(db.String(10))
    coffee_price = db.Column(db.String(10))
