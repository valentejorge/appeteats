"""Module providing a tools for register and login users"""
from datetime import datetime
from functools import wraps
from werkzeug.security import generate_password_hash
from flask import session, abort
from appetieats.ext.database import db
from appetieats.models import (
        Users, RestaurantsData, RestaurantOpeningHours, CustomersData
)


def login_required(role=None):
    """
    Decorate routes to require login and optionally a specific role.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_role = session.get("role")

            if user_role is None:
                return abort(403, "You must login to access this page")

            if role is not None and user_role != role:
                if role == "restaurant":
                    return abort(
                            403,
                            "Restricted Access: This page is exclusive for "
                            "restaurants. Please login with a restaurant "
                            "account to access it."
                    )
                if role == "customer":
                    return abort(
                            403,
                            "Restricted Access: This page is exclusive for "
                            "customers. Please login with a customer "
                            "account to access it."
                    )

            return f(*args, **kwargs)
        return decorated_function
    return decorator


def register_restaurant_user(user_data, weekdays):
    """register a restaurant"""
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
    """register a customer"""
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
    """log a user"""
    user = Users.query.filter_by(username=username).first() or abort(
            403, "fatal error")
    session["user_id"] = user.id
    session["role"] = user.role
