from flask import Blueprint
from flask_restful import Api

from .resources import ProductResource

bp = Blueprint("restapi", __name__, url_prefix="/api/")
api = Api(bp)


def init_app(app):
    api.add_resource(ProductResource, "/product/")
    app.register_blueprint(bp)
