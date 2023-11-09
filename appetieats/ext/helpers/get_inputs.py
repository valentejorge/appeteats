"""Module providing a functions for get inputs from users"""
from flask import request


def get_product_data_from_request():
    """get product data from request"""
    data = {}
    fields = {
            "name": str,
            "price": str,
            "description": str,
            "barcode": str,
            "category": str
    }
    for field, data_type in fields.items():
        data[field] = request.form.get(field, type=data_type)

    data["price"] = data["price"].replace("$ ", "")

    return data


def get_product_image(name):
    """get product image from request"""
    image = request.files[f"{name}"]
    return image


def get_restaurant_user_data():
    """get restaurant data from request"""
    form_data = {}

    fields = {
        "name": str,
        "address": str,
        "phone": str,
        "color": str,
        "url": str,
        "username": str,
        "password": str,
        "confirm": str,
        "everyday": str,
        "agree": bool
    }

    for field, data_type in fields.items():
        form_data[field] = request.form.get(field, type=data_type)

    if form_data["everyday"] is None:
        form_data["everyday"] = "off"

    return form_data


def get_customer_user_data():
    """get customer data from request"""
    form_data = {}

    fields = {
        "first-name": str,
        "last-name": str,
        "phone": str,
        "address": str,
        "zip-code": str,
        "reference": str,
        "username": str,
        "password": str,
        "confirm": str,
        "agree": bool
    }

    for field, data_type in fields.items():
        form_data[field] = request.form.get(field, type=data_type)

    return form_data


def get_passwords_fields():
    """get passwords fields from user"""
    data = {}

    fields = {
        "current": str,
        "new": str,
        "confirm": str
    }

    for field, data_type in fields.items():
        data[field] = request.form.get(field, type=data_type)

    print(data)
    return data


def get_opening_hours(is_open_everyday):
    """get opening hours data from request"""
    name_days = {"monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3,
                 "friday": 4, "saturday": 5, "sunday": 6}
    if is_open_everyday is True:
        weekdays = {day_int: {
            "is_open": request.form.get(day, type=bool),
            "open_at": request.form.get("open_everyday", type=str),
            "close_at": request.form.get("close_everyday", type=str)
            } for day, day_int in name_days.items()}
    else:
        weekdays = {day_int: {
            "is_open": request.form.get(day, type=bool),
            "open_at": request.form.get(f"open_{day}", type=str),
            "close_at": request.form.get(f"close_{day}", type=str)
            } for day, day_int in name_days.items()}

    return weekdays
