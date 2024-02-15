"""Module to configure the database"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_app(app):
    """init database"""
    db.init_app(app)
