from __future__ import annotations

from . import db
from .forms import CafeForm


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

    @staticmethod
    def create_from(form: CafeForm) -> Cafe:
        return Cafe(
            name=form.name.data,
            map_url=form.map_url.data,
            img_url=form.img_url.data,
            location=form.location.data,
            has_sockets=form.has_sockets.data == 'Yes',
            has_toilet=form.has_toilet.data == 'Yes',
            has_wifi=form.has_wifi.data == 'Yes',
            can_take_calls=form.can_take_calls.data == 'Yes',
            seats=form.seats.data,
            coffee_price=form.coffee_price.data
        )
