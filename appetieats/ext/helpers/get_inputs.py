from flask import request


def get_product_data_from_request():
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
    image = request.files[f"{name}"]
    return image


def get_restaurant_user_data():
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


def get_opening_hours(is_open_everyday):
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
