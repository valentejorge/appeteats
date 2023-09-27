from flask import Blueprint, render_template, request, redirect, session
from appetieats.ext.helper.register_tools import (
        register_restaurant_user, log_user, register_customer_user
)
from appetieats.ext.helper.get_inputs import (
        get_restaurant_user_data, get_opening_hours, get_customer_user_data
)
from appetieats.ext.helper.validate_inputs import (
        validate_user_register_data, validate_credentials, validate_user_data
)

auth_bp = Blueprint('auth', __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """Register a new restaurant"""
    if request.method == "POST":

        user_data = get_restaurant_user_data()
        week_opening_time = get_opening_hours(user_data["is_open_everyday"])

        validate_user_data(user_data)

        validate_user_register_data(user_data["username"],
                                    user_data["password"],
                                    user_data["confirm"])

        register_restaurant_user(user_data, week_opening_time)

        log_user(user_data["username"])
        print(user_data["username"])

        return redirect("/admin/dashboard")
    else:
        return render_template("auth/register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
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
        return render_template("auth/login.html")


@auth_bp.route("/customer/login", methods=["GET", "POST"])
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
            return redirect(f"/{last_restaurant}#cart")

    else:
        return render_template("auth/customer-login.html")


@auth_bp.route("/customer/register", methods=["GET", "POST"])
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
        return redirect("/customer/register")
    else:
        return render_template("auth/customer-register.html")


@auth_bp.route("/logout")
def logout():
    """Log user out"""

    session.clear()

    return redirect("/")


def init_app(app):
    app.register_blueprint(auth_bp)
