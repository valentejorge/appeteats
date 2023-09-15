from flask import (Blueprint, render_template, jsonify, request, flash,
                   redirect)
from appetieats.models import (RestaurantsData, Users, Categories, Products,
                               ProductImages)
from appetieats.ext.helper.cache_images import get_image
import json

menu_bp = Blueprint('menu', __name__)


@menu_bp.route("/<restaurant_user>", methods=['GET', 'POST'])
def index(restaurant_user):
    """Show the restaurant menu's page"""
    if request.method == "POST":
        products = Products.query.join(
                    Users, Products.user_id == Users.id
                ).filter(
                    Users.username == restaurant_user
                ).with_entities(
                    Products.id, Products.name, Products.price,
                    Products.user_id
                ).distinct().all()

        cart_data = request.form.get('cart-data')
        cart_dict = json.loads(cart_data)

        products_ids = {product.id for product in products}
        restaurant_id = products[0].user_id

        for item in cart_dict:
            if (
                item['id'] not in products_ids or
                item['restaurant_id'] != restaurant_id
            ):
                flash("Check your order and try again", "danger")
                return redirect(f'/{restaurant_user}#cart')

        link = 'https://google.com'

        flash(f"Success: check your <a href='{link}'>order</a>", "success")
        return redirect(f'/{restaurant_user}#cart')

    else:
        restaurant_info = RestaurantsData.query.join(
                Users, RestaurantsData.user_id == Users.id
                ).filter(Users.username == restaurant_user).first()
        """
        for value in restaurant_info.to_dict():
            print(f'{value}')
        """

        return render_template("menu/menu.html",
                               restaurant_info=restaurant_info)


@menu_bp.route("/<restaurant_user>/data")
def data(restaurant_user):
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


@menu_bp.route("/<restaurant_user>/order", methods=['GET', 'POST'])
def order(restaurant_user):
    """registry a order"""
    products = Products.query.join(
                Users, Products.user_id == Users.id
            ).filter(
                Users.username == restaurant_user
            ).with_entities(
                Products.id, Products.name, Products.price,
                Products.user_id
            ).distinct().all()

    products_ids = {product.id for product in products}
    restaurant_id = products[0].user_id

    cart_data = request.get_json()
    for item in cart_data:
        if item['id'] not in products_ids or item['restaurant_id'] != restaurant_id:
            print("não está")
        print(item)
        print(item['restaurant_id'])
    return flash("eita")
    return jsonify({"message": "Cart updated successfully"})
