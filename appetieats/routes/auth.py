from flask import Blueprint, render_template, request, redirect, session
from appetieats.ext.helpers import (verify_user_register_data, register_user,
                                    check_credentials, log_user)
from appetieats.ext.register_tools import take_user_data, take_opening_hours

auth_bp = Blueprint('auth', __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """Register a new restaurant"""
    if request.method == "POST":

        user_data = take_user_data()
        week_opening_time = take_opening_hours(user_data["is_open_everyday"])

        verify_user_register_data(user_data["username"], user_data["password"],
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
        check_credentials(username, password)
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
