from __future__ import annotations

from . import db
from .forms import CafeForm

from flask_login import UserMixin


def to_bool(yes_no: str) -> bool:
    return yes_no == 'True'


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

    def update_from(self, form: CafeForm) -> None:
        self.name = form.name.data
        self.map_url = form.map_url.data
        self.img_url = form.img_url.data
        self.location = form.location.data
        self.has_sockets = to_bool(form.has_sockets.data)
        self.has_toilet = to_bool(form.has_toilet.data)
        self.has_wifi = to_bool(form.has_wifi.data)
        self. can_take_calls = to_bool(form.can_take_calls.data)
        self. seats = form.seats.data
        self. coffee_price = form.coffee_price.data

    @staticmethod
    def create_from(form: CafeForm) -> Cafe:
        return Cafe(
            name=form.name.data,
            map_url=form.map_url.data,
            img_url=form.img_url.data,
            location=form.location.data,
            has_sockets=to_bool(form.has_sockets.data),
            has_toilet=to_bool(form.has_toilet.data),
            has_wifi=to_bool(form.has_wifi.data),
            can_take_calls=to_bool(form.can_take_calls.data),
            seats=form.seats.data,
            coffee_price=form.coffee_price.data
        )


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    has_admin_privileges = db.Column(db.Boolean, nullable=False)
