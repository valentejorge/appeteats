from functools import wraps
from flask import redirect, session, abort, request
from appetieats.models import Users, RestaurantsData, RestaurantOpeningHours
from appetieats.ext.database import db
from werkzeug.security import check_password_hash, generate_password_hash
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


def register_user(user_data, weekdays):
    psw_hash = generate_password_hash(user_data["password"])
    new_user = Users(username=user_data["username"], hash=psw_hash)
    db.session.add(new_user)
    db.session.commit()

    user_id = new_user.id

    restaurant = RestaurantsData(
            name=user_data["name"],
            address=user_data["address"],
            phone=user_data["phone"],
            color=user_data["color"],
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


def verify_user_register_data(username, password, confirm):
    if not username:
        return abort(403, "You must provide a username")

    elif not password:
        return abort(403, "You must provide a password")

    elif not confirm:
        return abort(403, "You must confirm your password")

    elif password != confirm:
        return abort(403, "The passwords dont match")

    elif Users.query.filter_by(username=username).first() is not None:
        return abort(403, "The username already exists")

    else:
        return


def check_credentials(username, password):
    user = Users.query.filter_by(username=username).first()

    if not username:
        return abort(403, "must provide username")

    elif not password:
        return abort(403, "must provide password")

    elif not user:
        return abort(403, "invalid user")

    elif not check_password_hash(user.hash, str(password)):
        return abort(403, "wrong password")

    else:
        return


def log_user(username):
    user = Users.query.filter_by(username=username).first() or abort(
            403, "fatal error")
    session["user_id"] = user.id
