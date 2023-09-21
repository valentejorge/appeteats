from flask import Blueprint, render_template, request, redirect, session
from appetieats.ext.helper.register_tools import register_user, log_user
from appetieats.ext.helper.get_inputs import get_user_data, get_opening_hours
from appetieats.ext.helper.validate_inputs import (validate_user_register_data,
                                                   validate_credentials)

auth_bp = Blueprint('auth', __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """Register a new restaurant"""
    if request.method == "POST":

        user_data = get_user_data()
        week_opening_time = get_opening_hours(user_data["is_open_everyday"])

        validate_user_register_data(user_data["username"],
                                    user_data["password"],
                                    user_data["confirm"])

        register_user(user_data, week_opening_time)

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
        validate_credentials(username, password)
        log_user(username)
        print(session.get("user_id"))
        return redirect("/admin/dashboard")
    else:
        return render_template("auth/login.html")


@auth_bp.route("/costumer/login", methods=["GET", "POST"])
def costumer_login():
    """Login costumer user"""
    session.clear()
    if request.method == "POST":

        # TODO: log costumer account
        return
    else:

        # TODO: render_template to login user
        return


@auth_bp.route("/customer/register", methods=["GET", "POST"])
def costumer_register():
    """Register costumer user"""
    session.clear()
    if request.method == "POST":

        # TODO: register costumer account
        print(request.form)
        return redirect("/customer/register")
    else:
        return render_template("auth/customer-register.html")


@auth_bp.route("/logout")
def logout():
    """Log user out"""

    session.clear()

    return redirect("/")
