from flask import Blueprint, render_template
from appetieats.models import RestaurantsData, Users, Categories, Products

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
    print(categories)

    products = Products.query.join(
            Users, Products.user_id == Users.id
            ).filter(Users.username == restaurant_user).all()
    """
    restaurant_dict = vars(restaurant_info)
    for attribute, value in restaurant_dict.items():
        print(attribute, ":", value)
    """
    categories_dict = vars(products[0])
    for attribute, value in categories_dict.items():
        print(attribute, ":", value)

    return render_template("menu/menu.html",
                           restaurant_info=restaurant_info,
                           categories=categories,
                           products=products)
