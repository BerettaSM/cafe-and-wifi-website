import sys
import inspect


def does_class_exist_in_models(cls):
    """
    This function checks if a particular class exists
    inside the 'models' module. This function will
    include imported classes inside the module into
    the check.

    :param cls: A class to check for.
    :return: True if class name exists inside module + imports, False otherwise.
    """
    from .models import __name__ as name
    cls_members = inspect.getmembers(sys.modules[name], inspect.isclass)
    cls_names = [item[1].__name__ for item in cls_members]
    return cls.__name__ in cls_names


def insert_dummy_data(database):
    import csv
    from random import choice
    from .models import Cafe, User, Comment
    with open('dummy_data_cafes.csv', encoding='UTF-8', newline='') as file:
        reader = csv.DictReader(file)
        dummy_cafe_entries = [
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
    database.session.bulk_save_objects(dummy_cafe_entries)
    from werkzeug.security import generate_password_hash
    with open('dummy_data_users.csv', encoding='UTF-8', newline='') as file:
        reader = csv.DictReader(file)
        dummy_user_entries = [
            User(
                email=row['email'],
                username=row['username'],
                password=generate_password_hash(row['password']),
                has_admin_privileges=row['has_admin_privileges'] == 'True'
            )
            for row in reader
        ]
    database.session.bulk_save_objects(dummy_user_entries)
    database.session.commit()
    users = User.query.filter_by(has_admin_privileges=False).all()
    cafes = Cafe.query.all()
    texts = [
        'Legal!', 'Empolgante!', 'Eu já estive nesse lugar ai!', 'Lugar tranquilo, bem da hora.',
        'Dica: Não bebam o café dai, tem gosto de terra fervida...', 'O wifi dai não presta',
        'O café dai é muito caro.', '10/10! Eu visitaria de novo.', 'O café é batizado, só pode!',
        'Tô com fome! Quero leite!', 'O banheiro ai tá sempre entupido, deve ser a empadinha.',
        'Nunca tem mesa disponível nesse lugar ai!', 'Era melhor ter ido ver o filme do Pelé!'
    ]
    comments = [
        Comment(
            text=choice(texts),
            author_id=choice(users).id,
            cafe_id=choice(cafes).id
        )
        for _ in range(75)
    ]
    database.session.bulk_save_objects(comments)
    database.session.commit()
