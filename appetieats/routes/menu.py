from flask import Blueprint, render_template, jsonify
from appetieats.models import (RestaurantsData, Users, Categories, Products,
                               ProductImages)
import os

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

    return render_template("menu/menu-shell.html",
                           restaurant_info=restaurant_info,
                           categories=categories,
                           products=products)

    return render_template("menu/menu.html",
                           restaurant_info=restaurant_info,
                           categories=categories,
                           products=products)


@menu_bp.route("/<restaurant_user>/data")
def products(restaurant_user):
    """json of products"""
    def get_image(image_name, image_id):
        CACHE_DIR = "appetieats/static/cache"
        cache_filepath = os.path.join(CACHE_DIR, image_name)
        if not os.path.exists(cache_filepath):
            image_data = ProductImages.query.get(image_id).image_data
            with open(cache_filepath, "wb") as f:
                f.write(image_data)

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
        print(product, product[5])

    print(products)
    return jsonify(
            {"products": ([dict(product) for product in products])},
            {"categories": ([dict(category) for category in categories])}
    )

    products = Products.query.join(
            Users, Products.user_id == Users.id
            ).join(
            ProductImages, Products.id == ProductImages.product_id
            ).filter(Users.username == restaurant_user).all()
    print(products)
    return jsonify(
            {"products": [product.to_dict() for product in products]}
    )
