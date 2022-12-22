from __future__ import annotations

import re

from flask_wtf import FlaskForm
from wtforms import StringField, URLField, SubmitField, SelectField, RadioField, HiddenField
from wtforms.validators import DataRequired, URL, Regexp

# ---- Regex ----
value_regex = re.compile(r'^£\d+\.\d{2}$')
# -- Validator --
not_null = DataRequired(message='Cannot be empty.')
valid_url = URL(message='Must be a valid URL.')
formatted_price = Regexp(regex=value_regex, message='Must be properly formatted. e.g.: £2.80')
# ---------------


class CafeForm(FlaskForm):
    id = HiddenField()
    name = StringField('Name', validators=[not_null])
    location = StringField('Location', validators=[not_null])
    img_url = URLField('Image URL', validators=[not_null, valid_url])
    map_url = URLField('Map URL', validators=[not_null, valid_url])
    coffee_price = StringField('Coffee price', validators=[not_null, formatted_price])
    seats = SelectField('Seats', choices=[
        ('0-10', '0-10 seats'),
        ('10-20', '10-20 seats'),
        ('20-30', '20-30 seats'),
        ('30-40', '30-40 seats'),
        ('40-50', '40-50 seats'),
        ('50+', '50+ seats'),
    ], validators=[not_null])
    has_sockets = RadioField('Has sockets', choices=[(True, 'Yes'), (False, 'No')])
    has_toilet = RadioField('Has toilet', choices=[(True, 'Yes'), (False, 'No')])
    has_wifi = RadioField('Has wifi', choices=[(True, 'Yes'), (False, 'No')])
    can_take_calls = RadioField('Can take calls', choices=[(True, 'Yes'), (False, 'No')])
    submit = SubmitField('Submit')

    @staticmethod
    def with_radio_defaults() -> CafeForm:
        form = CafeForm()
        form.has_wifi.default = False
        form.has_toilet.default = False
        form.has_sockets.default = False
        form.can_take_calls.default = False
        form.process()
        return form

    @staticmethod
    def populated_from(cafe) -> CafeForm:
        return CafeForm(
            id=cafe.id,
            name=cafe.name,
            location=cafe.location,
            img_url=cafe.img_url,
            map_url=cafe.map_url,
            coffee_price=cafe.coffee_price,
            seats=cafe.seats,
            has_sockets=cafe.has_sockets,
            has_toilet=cafe.has_toilet,
            has_wifi=cafe.has_wifi,
            can_take_calls=cafe.can_take_calls
        )
