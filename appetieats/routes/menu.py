from flask import (Blueprint, render_template, jsonify, request, flash,
                   redirect, session, abort)
from appetieats.models import (
        RestaurantsData, Users, Categories, Products, ProductImages
)
from appetieats.ext.helper.cache_images import get_image
import json

menu_bp = Blueprint('menu', __name__)


@menu_bp.route("/<restaurant_url>", methods=['GET', 'POST'])
def index(restaurant_url):
    """Show the restaurant menu's page"""
    restaurant = RestaurantsData.query.filter_by(url=restaurant_url).first()

    if not restaurant:
        return abort(404, "restaurant not found, check the url")

    if request.method == "POST":

        products = Products.query.join(
                    Users, Products.user_id == Users.id
                ).filter(
                    Users.id == restaurant.user_id
                ).with_entities(
                    Products.id, Products.name, Products.price,
                    Products.user_id
                ).distinct().all()

        cart_data = request.form.get('cart-data')
        cart_dict = json.loads(cart_data)

        products_ids = {product.id for product in products}
        restaurant_id = restaurant.user_id

        for item in cart_dict:
            if (
                item['id'] not in products_ids or
                item['restaurant_id'] != restaurant_id
            ):
                flash("Check your order and try again", "danger")
                return redirect(f'/{restaurant_url}#cart')

        if not session.get("costumer_id"):
            flash(
                "Error: To place an order, please " +
                "<a href='/customer/register'>Register</a> or " +
                "<a href='/customer/login'>Login</a>",
                "warning"
            )
            return redirect(f'/{restaurant_url}#cart')

        link = 'https://google.com'

        flash(f"Success: check your <a href='{link}'>order</a>", "success")
        return redirect(f"/{restaurant_url}#cart")

    else:
        restaurant_info = RestaurantsData.query.join(
                Users, RestaurantsData.user_id == Users.id
                ).filter(Users.id == restaurant.user_id).first()
        """
        for value in restaurant_info.to_dict():
            print(f'{value}')
        """

        return render_template(
                "menu/menu.html", restaurant_info=restaurant_info
        )


@menu_bp.route("/<restaurant_url>/data")
def data(restaurant_url):
    """Products data"""
    restaurant = RestaurantsData.query.filter_by(url=restaurant_url).first()

    if not restaurant:
        return abort(404, "restaurant not found, check the url")

    products = Products.query.join(
                Users, Products.user_id == Users.id
            ).join(
                ProductImages, Products.id == ProductImages.product_id
            ).join(
                Categories, Users.id == Categories.user_id
            ).filter(
                Users.id == restaurant.user_id
            ).with_entities(
                Products.id, Products.name, Products.price,
                Products.category_id, Products.description,
                ProductImages.id, ProductImages.image_path,
                Products.user_id
            ).distinct().all()

    categories = Categories.query.join(
                Users, Categories.user_id == Users.id
            ).filter(
                Users.id == restaurant.user_id
            ).with_entities(
                Categories.category_name, Categories.id
            ).distinct().all()

    for product in products:
        get_image(product.image_path, product[5])

    return jsonify(
            {"products": ([dict(product) for product in products])},
            {"categories": ([dict(category) for category in categories])}
    )


def init_app(app):
    app.register_blueprint(menu_bp)
