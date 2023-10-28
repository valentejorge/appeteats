"""Module to configure the application"""
from importlib import import_module
from dynaconf import FlaskDynaconf


def load_extensions(app):
    """load extensions from toml file"""
    for extension in app.config.get("EXTENSIONS"):
        mod = import_module(extension)
        mod.init_app(app)


def init_app(app):
    """init dynaconf"""
    FlaskDynaconf(app)
