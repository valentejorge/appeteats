"""Module for main routes"""
from flask import Blueprint, render_template, abort

main_bp = Blueprint('main', __name__)


@main_bp.route("/")
def index():
    """Show the landing page"""
    return render_template("landing.html")


@main_bp.route("/error")
def error():
    """Error message page"""
    a = None
    if not a:
        abort(404, "Error page is working! :)")
    return render_template("error.html")


def init_app(app):
    """init main blueprint"""
    app.register_blueprint(main_bp)
