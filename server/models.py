from __future__ import annotations

from datetime import datetime

from flask_login import UserMixin
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash

from . import db
from .utils import to_bool, formatted_timestamp


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
    comments = relationship(
        "Comment",
        back_populates="parent_cafe",
        order_by="desc(Comment.timestamp_create)"
    )

    def update_from(self, cafe_form) -> None:
        self.name = cafe_form.name.data
        self.map_url = cafe_form.map_url.data
        self.img_url = cafe_form.img_url.data
        self.location = cafe_form.location.data
        self.has_sockets = to_bool(cafe_form.has_sockets.data)
        self.has_toilet = to_bool(cafe_form.has_toilet.data)
        self.has_wifi = to_bool(cafe_form.has_wifi.data)
        self.can_take_calls = to_bool(cafe_form.can_take_calls.data)
        self.seats = cafe_form.seats.data
        self.coffee_price = cafe_form.coffee_price.data

    @staticmethod
    def create_from(cafe_form) -> Cafe:
        return Cafe(
            name=cafe_form.name.data,
            map_url=cafe_form.map_url.data,
            img_url=cafe_form.img_url.data,
            location=cafe_form.location.data,
            has_sockets=to_bool(cafe_form.has_sockets.data),
            has_toilet=to_bool(cafe_form.has_toilet.data),
            has_wifi=to_bool(cafe_form.has_wifi.data),
            can_take_calls=to_bool(cafe_form.can_take_calls.data),
            seats=cafe_form.seats.data,
            coffee_price=cafe_form.coffee_price.data
        )


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    has_admin_privileges = db.Column(db.Boolean, nullable=False)
    comments = relationship("Comment", back_populates="comment_author")

    @staticmethod
    def create_from(user_form) -> User:
        return User(
            email=user_form.signup_email.data,
            username=user_form.signup_username.data,
            password=generate_password_hash(user_form.signup_password.data),
            has_admin_privileges=False
        )


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    timestamp_create = db.Column(db.String(50), default=formatted_timestamp)
    timestamp_update = db.Column(db.String(50), onupdate=formatted_timestamp)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    comment_author = relationship("User", back_populates="comments")
    cafe_id = db.Column(db.Integer, db.ForeignKey("cafe.id"))
    parent_cafe = relationship("Cafe", back_populates="comments")
