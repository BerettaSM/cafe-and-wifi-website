

def insert_dummy_data(database):
    import csv
    from .models import Cafe, User
    with open('entries.csv', encoding='UTF-8', newline='') as file:
        reader = csv.DictReader(file)
        dummy_entries = [
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
    database.session.bulk_save_objects(dummy_entries)
    from werkzeug.security import generate_password_hash
    database.session.add(
        User(
            email='admin@admin.com',
            password=generate_password_hash('admin'),
            first_name='Admin',
            last_name='The Admin',
            has_admin_privileges=True
        )
    )
    database.session.add(
        User(
            email='user@user.com',
            password=generate_password_hash('user'),
            first_name='John',
            last_name='Doe',
            has_admin_privileges=False
        )
    )
    database.session.commit()
