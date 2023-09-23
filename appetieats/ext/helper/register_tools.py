from functools import wraps
from flask import redirect, session, abort
from appetieats.models import (
        Users, RestaurantsData, RestaurantOpeningHours, CustomersData
)
from appetieats.ext.database import db
from werkzeug.security import generate_password_hash
from datetime import datetime


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def register_restaurant_user(user_data, weekdays):
    psw_hash = generate_password_hash(user_data["password"])
    new_user = Users(
            username=user_data["username"], hash=psw_hash, role="restaurant"
    )
    db.session.add(new_user)
    db.session.commit()

    user_id = new_user.id

    restaurant = RestaurantsData(
            name=user_data["name"],
            address=user_data["address"],
            phone=user_data["phone"],
            color=user_data["color"],
            url=user_data["url"],
            user_id=user_id
    )
    db.session.add(restaurant)
    db.session.commit()

    for i, hours in weekdays.items():
        if hours["is_open"]:
            opening_time = datetime.strptime(hours["open_at"], "%H:%M").time()
            closing_time = datetime.strptime(hours["close_at"], "%H:%M").time()

            opening_hours = RestaurantOpeningHours(
                    restaurant_id=restaurant.id,
                    day_of_week=i,
                    opening_time=opening_time,
                    closing_time=closing_time
                    )
            db.session.add(opening_hours)
            db.session.commit()


def register_customer_user(user_data):
    psw_hash = generate_password_hash(user_data["password"])
    new_user = Users(
            username=user_data["username"], hash=psw_hash, role="customer"
    )
    db.session.add(new_user)
    db.session.commit()

    user_id = new_user.id

    customer = CustomersData(
            first_name=user_data["first-name"],
            last_name=user_data["last-name"],
            phone=user_data["phone"],
            address=user_data["address"],
            zip_code=user_data["zip-code"],
            reference=user_data["reference"],
            user_id=user_id
    )
    db.session.add(customer)
    db.session.commit()


def log_user(username):
    user = Users.query.filter_by(username=username).first() or abort(
            403, "fatal error")
    session["user_id"] = user.id
    session["account_type"] = user.role
