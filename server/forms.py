from __future__ import annotations

import re

from flask_wtf import FlaskForm
from wtforms import EmailField, HiddenField, PasswordField, RadioField
from wtforms import SelectField, StringField, SubmitField, TextAreaField, URLField
from wtforms.validators import URL, Regexp, Email, Length, EqualTo, DataRequired

from .custom_validators import UniqueUserEmail, UniqueUsername

# ---- Regex ----
multiple_spaces_regex = re.compile(r'\s{2,}')
value_regex = re.compile(r'^£\d+\.\d{2}$')
# -- Validator --
not_null = DataRequired(message='Cannot be empty.')
valid_url = URL(message='Must be a valid URL.')
valid_email = Email(message='Must be a valid email.')
unique_email = UniqueUserEmail(message='This email is already registered.')
unique_username = UniqueUsername(message='This username is already registered.')
valid_username_length = Length(min=4, message='Must have a minimum length of 4 characters.')
valid_password_length = Length(min=8, message='Must have a minimum length of 8 characters.')
comment_text_length = Length(max=2000, message='Must have a maximum length of 2000 characters.')
formatted_price = Regexp(regex=value_regex, message='Must be properly formatted. e.g.: £2.80')
# ---------------


def my_strip_filter(value):
    """This filter strips whitespaces and transforms
    chains of multiple whitespaces into a single whitespace."""
    if value is not None and hasattr(value, 'strip'):
        return multiple_spaces_regex.sub(' ', value.strip())
    return value


class BaseForm(FlaskForm):
    class Meta:
        def bind_field(self, form, unbound_field, options):
            filters = unbound_field.kwargs.get('filters', [])
            filters.append(my_strip_filter)
            return unbound_field.bind(form=form, filters=filters, **options)


class CafeForm(BaseForm):
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


class UserForm(BaseForm):
    signup_email = EmailField('Email', validators=[not_null, valid_email, unique_email])
    signup_username = StringField('Username', validators=[not_null, valid_username_length, unique_username])
    signup_password = PasswordField('New Password', validators=[
        not_null, valid_password_length, EqualTo('signup_confirm', message='Passwords must match!')
    ])
    signup_confirm = PasswordField('Repeat password', validators=[
        not_null, valid_password_length, EqualTo('signup_password', message='Passwords must match!')
    ])
    submit = SubmitField('Sign-Up')


class CommentForm(BaseForm):
    text = TextAreaField('Leave a comment', validators=[not_null, comment_text_length])
    send = SubmitField('Send')
