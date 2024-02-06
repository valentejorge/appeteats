"""Module to configure the sessions"""
from flask_session import Session


def init_app(app):
    """
    Ensure templates are auto-reloaded
    and config session to use filesystem
    (instead of signed cookies)
    """

    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)
