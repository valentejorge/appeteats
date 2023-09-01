from flask import request


def take_user_data():
    form_data = {}

    fields = {
        "name": str,
        "address": str,
        "phone": str,
        "color": str,
        "username": str,
        "password": str,
        "confirm": str,
        "is_open_everyday": bool,
        "agree": bool
    }

    for field, data_type in fields.items():
        form_data[field] = request.form.get(field, type=data_type)

    return form_data


def take_opening_hours(is_open_everyday):
    name_days = {"monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3,
                 "friday": 4, "saturday": 5, "sunday": 6}
    if is_open_everyday:
        weekdays = {day_int: {
            "is_open": request.form.get(day, type=bool),
            "open_at": request.form.get("open_everyday", type=str),
            "close_at": request.form.get("close_everyday", type=str)
            } for day, day_int in name_days}
    else:
        weekdays = {day_int: {
            "is_open": request.form.get(day, type=bool),
            "open_at": request.form.get(f"open_{day}", type=str),
            "close_at": request.form.get(f"close_{day}", type=str)
            } for day, day_int in name_days.items()}
    return weekdays
