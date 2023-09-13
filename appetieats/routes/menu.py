from flask import Blueprint, render_template, jsonify
from appetieats.models import (RestaurantsData, Users, Categories, Products,
                               ProductImages)
from appetieats.ext.helper.cache_images import get_image

menu_bp = Blueprint('menu', __name__)


@menu_bp.route("/<restaurant_user>")
def index(restaurant_user):
    """Show the restaurant menu's page"""

    restaurant_info = RestaurantsData.query.join(
            Users, RestaurantsData.user_id == Users.id
            ).filter(Users.username == restaurant_user).first()

    return render_template("menu/menu.html",
                           restaurant_info=restaurant_info)


@menu_bp.route("/<restaurant_user>/data")
def products(restaurant_user):
    """Products data"""

    products = Products.query.join(
                Users, Products.user_id == Users.id
            ).join(
                ProductImages, Products.id == ProductImages.product_id
            ).join(
                Categories, Users.id == Categories.user_id
            ).filter(
                Users.username == restaurant_user
            ).with_entities(
                Products.id, Products.name, Products.price,
                Products.category_id, Products.description,
                ProductImages.id, ProductImages.image_path,
                Products.user_id
            ).distinct().all()

    categories = Categories.query.join(
                Users, Categories.user_id == Users.id
            ).filter(
                Users.username == restaurant_user
            ).with_entities(
                Categories.category_name, Categories.id
            ).distinct().all()

    for product in products:
        get_image(product.image_path, product[5])

    return jsonify(
            {"products": ([dict(product) for product in products])},
            {"categories": ([dict(category) for category in categories])}
    )
