import json
import os
from appetieats.ext.database import db
from appetieats.models import (
        Users, RestaurantsData, Categories, ProductImages, Products,
        CustomersData
)
from werkzeug.security import generate_password_hash


def create_db():
    """create sql database"""
    db.create_all()


def drop_db():
    """drop sql database"""
    db.drop_all()


def populate_database_from_json():
    json_file = 'appetieats/ext/helpers/sample_data.json'
    print(os.path.abspath(json_file))

    with open(json_file, 'r') as file:
        data = json.load(file)

        for user_data in data['users']:
            user_data['hash'] = generate_password_hash(user_data['hash'])
            user = Users(**user_data)
            db.session.add(user)

        for restaurant_data in data['restaurants']:
            restaurant = RestaurantsData(**restaurant_data)
            db.session.add(restaurant)

        for categories_data in data['categories']:
            category = Categories(**categories_data)
            db.session.add(category)

        for customer_data in data['customers']:
            customer = CustomersData(**customer_data)
            db.session.add(customer)

        for product_data in data['products']:
            product = Products(**product_data)
            db.session.add(product)

        for image_data in data['product_images']:
            image_path = image_data['image_path']
            product_id = image_data['product_id']

            product_image = ProductImages(
                product_id=product_id,
                image_path=image_path,
                image_data=open(
                    f"appetieats/static/sample_data/{image_path}", "rb"
                    ).read()
            )
            db.session.add(product_image)

        db.session.commit()


def hello_commands():
    """says hello"""
    print("hello commands")


def restart_db():
    """restart database"""
    drop_db()
    create_db()
    populate_database_from_json()


def init_app(app):
    """add multiple commands in a bulk"""
    for command in [create_db,
                    drop_db,
                    populate_database_from_json,
                    hello_commands,
                    restart_db]:
        app.cli.add_command(app.cli.command()(command))
    return app
