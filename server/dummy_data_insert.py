def insert_dummy_data(database):
    import csv
    from os import path
    from random import choice
    from .models import Cafe, User, Comment
    curr_dir = path.dirname(__file__)
    with open(path.join(curr_dir, 'dummy_data/dummy_data_cafes.csv'), encoding='UTF-8', newline='') as file:
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
    with open(path.join(curr_dir, 'dummy_data/dummy_data_users.csv'), encoding='UTF-8', newline='') as file:
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
    with open(path.join(curr_dir, 'dummy_data/dummy_data_comments.csv'), encoding='UTF-8', newline='') as file:
        dummy_comment_entries = [line.strip() for line in file.readlines()]
    comments = [
        Comment(
            text=choice(dummy_comment_entries),
            author_id=choice(users).id,
            cafe_id=choice(cafes).id
        )
        for _ in range(75)
    ]
    database.session.bulk_save_objects(comments)
    database.session.commit()
