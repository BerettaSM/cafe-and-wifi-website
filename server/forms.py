from wtforms import Form, StringField, SubmitField, URLField, BooleanField


class CafeForm(Form):
    name = StringField('Name:')
    map_url = URLField('Map URL:')
    img_url = URLField('Image URL:')
    location = StringField('Location: ')
    has_sockets = BooleanField('Has sockets:')
    has_toilet = BooleanField('Has toilet:')
    has_wifi = BooleanField('Has wifi:')
    can_take_calls = BooleanField('Can take calls:')
    seats = StringField('Seats:')
    coffee_price = StringField('Coffee price:')
    submit = SubmitField('Submit')
