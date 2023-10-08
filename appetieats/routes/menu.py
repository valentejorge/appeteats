from flask import (
        Blueprint, render_template, jsonify, request, flash, redirect,
        session, abort
)
from appetieats.models import (
        RestaurantsData, Users, Categories, Products, ProductImages
)
from appetieats.ext.helper.validate_inputs import (
        validate_cart, validate_user_account
)
from appetieats.ext.helper.cache_images import get_image
from appetieats.ext.helper.db_tools import add_new_oder
import json

menu_bp = Blueprint('menu', __name__)


@menu_bp.route("/<restaurant_url>", methods=['GET', 'POST'])
def index(restaurant_url):
    """Show the restaurant menu's page"""
    restaurant = RestaurantsData.query.filter_by(url=restaurant_url).first()

    if not restaurant:
        return abort(404, "restaurant not found, check the url")

    session["last_restaurant"] = restaurant_url

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

        product_price_dict = {
                product.id: product.price for product in products
        }

        total = 0
        for item in cart_dict:
            item["price"] = product_price_dict.get(item["id"])
            item["sub_total"] = item["price"]*item["quantity"]
            total += item["sub_total"]

        restaurant_id = restaurant.user_id

        if not validate_cart(products, cart_dict, restaurant_id):
            flash("Check your order and try again", "danger")
            return redirect(f'/{restaurant_url}#cart')

        if not validate_user_account():
            flash(
                "Error: To place an order, please " +
                "<a href='/register/customer'>Register</a> or " +
                "<a href='/login/customer'>Login</a>", "warning"
            )
            return redirect(f'/{restaurant_url}#cart')

        # TODO: add the new order in database
        customer_id = session.get("user_id")
        add_new_oder(customer_id, restaurant_id, total, cart_dict)

        flash(
            "Success: check your <a href='/customer'>orders</a>",
            "success"
        )
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
        product_id = product[5]
        get_image(product.image_path, product_id)

    return jsonify(
            {"products": ([dict(product) for product in products])},
            {"categories": ([dict(category) for category in categories])}
    )


def init_app(app):
    app.register_blueprint(menu_bp)
