"""Module providing a commands to flask"""
import os
import json
from datetime import datetime
from werkzeug.security import generate_password_hash
from appetieats.ext.database import db
from appetieats.models import (
        Users, RestaurantsData, Categories, ProductImages, Products,
        CustomersData, RestaurantOpeningHours
)
from flask import current_app


def create_db():
    """create sql database"""
    db.create_all()


def drop_db():
    """drop sql database"""
    db.drop_all()


def populate_database_from_json(json_path):
    """populate db from a json file"""
    print(os.path.abspath(json_path))
    # print(current_app.config.get("TESTING"))
    # print(settings.JSON_DATA_PATH)
    if json_path[0] == '.':
        path_context = '../'
    else:
        path_context = 'appetieats/'

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
                                f"{path_context}/static/sample_data/{image_path}", "rb"
                                ).read()
                        )
                        db.session.add(product_image)
                    case "open_time":
                        opening_time = datetime.strptime(
                                data["opening_time"], "%H:%M").time()
                        closing_time = datetime.strptime(
                                data["closing_time"], "%H:%M").time()

                        time = RestaurantOpeningHours(
                                id=data["id"],
                                restaurant_id=data["restaurant_id"],
                                open=data["open"],
                                day_of_week=data["day_of_week"],
                                opening_time=opening_time,
                                closing_time=closing_time,
                        )
                        db.session.add(time)

        db.session.commit()


def hello_commands():
    """says hello"""
    hello = "hello commands"
    print(hello)
    return hello


def restart_db():
    """restart database"""
    drop_db()
    create_db()

    # path = "appetieats/ext/helpers/sample_data.json"
    path = current_app.config.get("JSON_DATA_PATH")
    populate_database_from_json(path)


def restart_testing_db():
    """restart database for tests"""
    drop_db()
    create_db()

    # path = "../ext/helpers/test_sample_data.json"
    path = current_app.config.get("JSON_DATA_PATH")
    populate_database_from_json(path)


def init_app(app):
    """add multiple commands in a bulk"""
    for command in [create_db,
                    drop_db,
                    populate_database_from_json,
                    hello_commands,
                    restart_db]:
        app.cli.add_command(app.cli.command()(command))
    return app
