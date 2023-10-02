from flask import Blueprint, render_template, request, redirect, session
from appetieats.ext.helper.register_tools import (
        register_restaurant_user, log_user, register_customer_user
)
from appetieats.ext.helper.get_inputs import (
        get_restaurant_user_data, get_opening_hours, get_customer_user_data
)
from appetieats.ext.helper.validate_inputs import (
        validate_user_register_data, validate_credentials, validate_user_data,
        validate_user_url
)

auth_bp = Blueprint('auth', __name__)


@auth_bp.route("/login")
def login():
    """Redirect user for especific login page"""
    return render_template("auth/redirect-login.html")


@auth_bp.route("/register")
def register():
    """Redirect user for especific register page"""
    return render_template("auth/redirect-register.html")


@auth_bp.route("/register/restaurant", methods=["GET", "POST"])
def restaurant_register():
    """Register a new restaurant"""
    if request.method == "POST":

        user_data = get_restaurant_user_data()
        week_opening_time = get_opening_hours(user_data["everyday"])

        validate_user_url(user_data["url"])

        validate_user_data(user_data)

        validate_user_register_data(
                user_data["username"],
                user_data["password"],
                user_data["confirm"]
        )

        register_restaurant_user(user_data, week_opening_time)

        log_user(user_data["username"])

        return redirect("/admin/dashboard")
    else:
        return render_template("auth/restaurant-register.html")


@auth_bp.route("/login/restaurant", methods=["GET", "POST"])
def restaurant_login():
    """Login user"""
    session.clear()

    if request.method == "POST":
        username, password = (
                request.form.get("username", type=str),
                request.form.get("password", type=str)
        )
        account_type = "restaurant"

        validate_credentials(username, password, account_type)
        log_user(username)

        print(session.get("user_id"), session.get("account_type"))
        return redirect("/admin/dashboard")
    else:
        return render_template("auth/restaurant-login.html")


@auth_bp.route("/register/customer", methods=["GET", "POST"])
def costumer_register():
    """Register customer user"""
    session.clear()
    if request.method == "POST":

        user_data = get_customer_user_data()

        validate_user_data(user_data)

        validate_user_register_data(
                user_data["username"],
                user_data["password"],
                user_data["confirm"]
        )

        register_customer_user(user_data)

        log_user(user_data["username"])
        print(session.get("user_id"), session.get("account_type"))

        return redirect("/admin/dashboard")
    else:
        return render_template("auth/customer-register.html")


@auth_bp.route("/login/customer", methods=["GET", "POST"])
def costumer_login():
    """Login customer user"""
    if request.method == "POST":

        username, password = (
                request.form.get("username", type=str),
                request.form.get("password", type=str)
        )

        account_type = "customer"

        validate_credentials(username, password, account_type)

        last_restaurant = session.get("last_restaurant")
        session.clear()

        log_user(username)
        if last_restaurant:
            return redirect(f"/{last_restaurant}#cart")
        else:
            return redirect("/customer")

    else:
        return render_template("auth/customer-login.html")


@auth_bp.route("/logout")
def logout():
    """Log user out"""

    session.clear()

    return redirect("/")


def init_app(app):
    app.register_blueprint(auth_bp)
