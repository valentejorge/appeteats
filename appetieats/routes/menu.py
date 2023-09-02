from flask import Blueprint, render_template, jsonify
from appetieats.models import (RestaurantsData, Users, Categories, Products,
                               ProductImages)

menu_bp = Blueprint('menu', __name__)


@menu_bp.route("/<restaurant_user>")
def index(restaurant_user):
    """Show the restaurant menu's page"""

    restaurant_info = RestaurantsData.query.join(
            Users, RestaurantsData.user_id == Users.id
            ).filter(Users.username == restaurant_user).first()

    categories = Categories.query.join(
            Users, Categories.user_id == Users.id
            ).filter(Users.username == restaurant_user).all()

    products = Products.query.join(
            Users, Products.user_id == Users.id
            ).filter(Users.username == restaurant_user).all()

    return render_template("menu/menu.html",
                           restaurant_info=restaurant_info,
                           categories=categories,
                           products=products)


@menu_bp.route("/<restaurant_user>/products")
def products(restaurant_user):
    """json of products"""

    products = Products.query.join(
                Users, Products.user_id == Users.id
            ).join(
                ProductImages, Products.id == ProductImages.product_id
            ).filter(
                Users.username == restaurant_user
            ).with_entities(
                Products.id, Products.name, Products.price,
                Categories.category_name, Products.description,
                ProductImages.image_path
            ).all()
    return jsonify({"products": ([dict(product) for product in products])})

    products = Products.query.join(
            Users, Products.user_id == Users.id
            ).join(
            ProductImages, Products.id == ProductImages.product_id
            ).filter(Users.username == restaurant_user).all()
    print(products)
    return jsonify(
            {"products": [product.to_dict() for product in products]}
    )
