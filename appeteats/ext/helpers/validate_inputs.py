"""Module providing a tools for validate user inputs"""
from flask import abort, session
from werkzeug.security import check_password_hash
from appeteats.models import Categories, Users, RestaurantsData


def validate_product_data(product_data):
    """validate data of product"""
    if not product_data["name"]:
        return abort(403, "You must provide a product name")

    if not product_data["price"]:
        return abort(403, "You must provide a price")

    if not str(product_data["price"]).replace('.', '', 1).isdigit():
        return abort(403, "You must provide a valid price")

    if not product_data["description"]:
        return abort(403, "You must provide a description")

    if not product_data["barcode"]:
        return abort(403, "You must provide a barcode")

    if not product_data["category"]:
        return abort(403, "You must provide a category")

    if Categories.query.filter_by(
            id=product_data["category"],
            user_id=session.get("user_id")).first() is None:
        return abort(403, "You must provide a valid category")

    return None


def validate_product_image(product_image):
    """validate image of product"""
    if not product_image:
        return abort(403, "You must provide a product image")
    return None


def validate_user_register_data(username, password, confirm):
    """validate data of user"""
    if not username:
        return abort(403, "You must provide a username")

    if not password:
        return abort(403, "You must provide a password")

    if not confirm:
        return abort(403, "You must confirm your password")

    if password != confirm:
        return abort(403, "The passwords dont match")

    if Users.query.filter_by(username=username).first() is not None:
        return abort(403, "The username already exists")

    return None


def validate_credentials(username, password, account_type):
    """validate credentials of user"""
    user = Users.query.filter_by(username=username).first()

    if not username or not password:
        return abort(403, "Must provide username/password")

    if not user:
        return abort(403, "Invalid user")

    if user.role != account_type:
        if account_type == "restaurant":
            return abort(
                    403,
                    "Your account is of customer type. "
                    "Please log in with a restaurant account"
            )
        if account_type == "customer":
            return abort(
                    403,
                    "Your account is of restaurant type. "
                    "Please log in with a customer account"
            )

    if not check_password_hash(user.hash, str(password)):
        return abort(403, "Wrong password")

    return None


def validate_user_data(user_data):
    """validate all inputs from user form"""
    for value in user_data.values():
        if not value:
            return abort(
                    403,
                    "You are attempting to register a restaurant account in "
                    "the customer route or vice versa."
            )

    return None


def validate_cart(products, cart_dict, restaurant_id):
    """validate products of cart"""
    products_ids = {product.id for product in products}
    if len(cart_dict) == 0:
        return False
    for item in cart_dict:
        if item["id"] not in products_ids:
            return False

        if item["restaurant_id"] != restaurant_id:
            return False

    return True


def validate_user_account():
    """validate user account"""
    if not session.get("user_id"):
        return False
    if not session.get("role") == "customer":
        return False
    return True


def validate_user_url(user_url):
    """validate user url"""
    url = RestaurantsData.query.filter_by(url=user_url).first()

    if url:
        return abort(403, "the url already exists, try another")

    return None


def validate_passwords(user_id, passwords):
    """validate passwords"""

    for password in passwords.values():
        print(password)
        if not password:
            return abort(403, "passwords fields cannot be empty")

    current_hash = Users.query.get(user_id).hash

    if not check_password_hash(current_hash, passwords["current"]):
        return abort(403, "current password wrong")

    if passwords["new"] != passwords["confirm"]:
        return abort(403, "new password and confirm need be the same")

    return None


def prevents_empty_fields(data):
    """prevents empty fields"""
    for d in data.values():
        if not d:
            return abort(403, "fields cannot be empty")


def validate_opening_time(weekdays_time_data):
    """validate opening time values"""
    for day in weekdays_time_data.values():
        if day["open"]:
            if not day["open_time"] or not day["close_time"]:
                return abort(403, "a marked time field cannot be empty")
    return None
