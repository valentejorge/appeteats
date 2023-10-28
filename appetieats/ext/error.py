"""Module to configure the error page"""
from flask import render_template


def init_app(app):
    """error page"""
    @app.errorhandler(404)
    @app.errorhandler(403)
    @app.errorhandler(500)
    def handle_error(error):
        error_code = error.code
        error_name = error.name
        error_description = error.description
        return render_template("error.html", error_code=error_code,
                               error_description=error_description,
                               error_name=error_name), error_code
