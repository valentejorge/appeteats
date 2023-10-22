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
    json_file = 'appetieats/ext/helper/sample_data.json'
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
                # TODO: change image path to a real path
                image_data=open(
                    "appetieats/static/assets/img/pizza.png", "rb"
                    ).read()
            )
            db.session.add(product_image)

        db.session.commit()


def populate_users():
    """populate db users with default accounts"""
    data = [
            Users(
                id=1,
                username="dev",
                hash=generate_password_hash("dev"),
                role="restaurant"
            ),
            RestaurantsData(
                id=1,
                name="Python Pizza",
                address="123 Snake St, Pythonville, PY 31415",
                phone="555-PY-314",
                color="#4B8BBE",
                url="python-pizza",
                user_id=1
            ),
            Users(
                id=2,
                username="wanteat",
                hash=generate_password_hash("wanteat"),
                role="customer"
            ),
            CustomersData(
                id=1,
                first_name="want",
                last_name="eat",
                phone="555-hungry",
                address="Craving St, 789",
                zip_code="98765",
                reference="near to rumbling belly",
                user_id=2
            ),
            Categories(
                id=1,
                user_id=1,
                category_name="Pizza"
            ),
            ProductImages(
                id=1,
                product_id=1,
                image_path="product1.png",
                image_data=open(
                    "appetieats/static/assets/img/pizza.png", "rb"
                    ).read()
            ),
            ProductImages(
                id=2,
                product_id=2,
                image_path="product2.png",
                image_data=open(
                    "appetieats/static/assets/img/pizza.png", "rb"
                    ).read()
            ),
            ProductImages(
                id=3,
                product_id=3,
                image_path="product3.png",
                image_data=open(
                    "appetieats/static/assets/img/pizza.png", "rb"
                    ).read()
            ),
            Products(
                id=1,
                name="Flask 'n' Cheese Pizza",
                description="A classic pizza with tomato "
                "sauce and melted cheese. A tribute to Flask, a lightweight "
                "Python web framework.",
                price=10.99,
                barcode=1,
                available="True",
                category_id=1,
                user_id=1
            ),
            Products(
                id=2,
                name="Python Pepperoni Powerhouse",
                description="A pepperoni lover's dream with generous slices "
                "of pepperoni. Pay homage to the mighty Python programming "
                "language.",
                price=14.99,
                barcode=2,
                available="True",
                category_id=1,
                user_id=1
            ),
            Products(
                id=3,
                name="Pythonic Pineapple Paradise",
                description="A sweet and savory blend of pineapple and ham "
                "with a Pythonic twist.",
                price=13.99,
                barcode=3,
                available="True",
                category_id=1,
                user_id=1
            )
    ]
    db.session.bulk_save_objects(data)
    db.session.commit()
    return Users.query.all()


def hello_commands():
    """says hello"""
    print("hello commands")


def restart_db():
    """restart database"""
    drop_db()
    create_db()
    populate_database_from_json()
    # populate_users()


def init_app(app):
    """add multiple commands in a bulk"""
    for command in [create_db,
                    drop_db,
                    populate_users,
                    hello_commands,
                    restart_db]:
        app.cli.add_command(app.cli.command()(command))
    return app
