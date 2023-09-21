from flask import abort, session
from appetieats.models import Categories, Users
from werkzeug.security import check_password_hash


def validate_product_data(product_data):
    if not product_data["name"]:
        return abort(403, "You must provide a product name")

    elif not product_data["price"]:
        return abort(403, "You must provide a price")

    elif not str(product_data["price"]).replace('.', '', 1).isdigit():
        return abort(403, "You must provide a valid price")

    elif not product_data["description"]:
        return abort(403, "You must provide a description")

    elif not product_data["barcode"]:
        return abort(403, "You must provide a barcode")

    elif not product_data["category"]:
        return abort(403, "You must provide a category")

    elif Categories.query.filter_by(
            id=product_data["category"],
            user_id=session.get("user_id")).first() is None:
        return abort(403, "You must provide a valid category")
    else:
        return


def validate_product_image(product_image):
    if not product_image:
        return abort(403, "You must provide a product image")
    else:
        return


def validate_user_register_data(username, password, confirm):
    if not username:
        return abort(403, "You must provide a username")

    elif not password:
        return abort(403, "You must provide a password")

    elif not confirm:
        return abort(403, "You must confirm your password")

    elif password != confirm:
        return abort(403, "The passwords dont match")

    elif Users.query.filter_by(username=username).first() is not None:
        return abort(403, "The username already exists")

    else:
        return


def validate_credentials(username, password):
    user = Users.query.filter_by(username=username).first()

    if not username:
        return abort(403, "must provide username")

    elif not password:
        return abort(403, "must provide password")

    elif not user:
        return abort(403, "invalid user")

    elif not check_password_hash(user.hash, str(password)):
        return abort(403, "wrong password")

    else:
        return
