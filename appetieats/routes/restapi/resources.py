from flask import abort, jsonify
from flask_restful import Resource

from appetieats.models import Products


class ProductResource(Resource):
    def get(self):
        products = Products.query.all() or abort(204)
        return jsonify(
                {"products": [product.to_dict() for product in products]}
        )
