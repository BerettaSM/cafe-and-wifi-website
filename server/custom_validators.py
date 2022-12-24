from wtforms.validators import ValidationError


class UniqueUserEmail:

    def __init__(self, message=None):
        self.message = message if message else f'Email already exists.'

    def __call__(self, form, field):
        from .models import User
        db_entry = User.query.filter_by(email=field.data).first()
        if db_entry is not None:
            raise ValidationError(self.message)


class UniqueUsername:

    def __init__(self, message=None):
        self.message = message if message else f'Username already exists.'

    def __call__(self, form, field):
        from .models import User
        db_entry = User.query.filter_by(username=field.data).first()
        if db_entry is not None:
            raise ValidationError(self.message)
