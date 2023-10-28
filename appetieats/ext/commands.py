"""Module providing a commands to flask"""
import os
import json
from werkzeug.security import generate_password_hash
from appetieats.ext.database import db
from appetieats.models import (
        Users, RestaurantsData, Categories, ProductImages, Products,
        CustomersData
)


def create_db():
    """create sql database"""
    db.create_all()


def drop_db():
    """drop sql database"""
    db.drop_all()


def populate_database_from_json():
    """populate db from a json file"""
    json_path = "appetieats/ext/helpers/sample_data.json"
    print(os.path.abspath(json_path))

    with open(json_path, "r", encoding="utf-8") as file:
        json_file = json.load(file)

        for key in json_file:
            for data in json_file[f"{key}"]:
                match key:
                    case "users":
                        data["hash"] = generate_password_hash(data["hash"])
                        user = Users(**data)
                        db.session.add(user)

                    case "restaurants":
                        restaurant = RestaurantsData(**data)
                        db.session.add(restaurant)

                    case "categories":
                        category = Categories(**data)
                        db.session.add(category)

                    case "customers":
                        customer = CustomersData(**data)
                        db.session.add(customer)

                    case "products":
                        product = Products(**data)
                        db.session.add(product)

                    case "product_images":
                        image_path = data["image_path"]
                        product_id = data["product_id"]

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
