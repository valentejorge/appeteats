"""Module for settings routes"""
from flask import (
        Blueprint, render_template, request, redirect, flash, session, abort
)
from appeteats.models import Categories, Products, RestaurantsData
from appeteats.ext.database import db

from appeteats.ext.helpers.register_tools import login_required
from appeteats.ext.helpers.get_inputs import (
        get_product_data_from_request, get_product_image, get_data_from_form
)
from appeteats.ext.helpers.validate_inputs import (
        validate_product_data, validate_product_image, validate_passwords,
        prevents_empty_fields
)
from appeteats.ext.helpers.db_tools import (
        add_new_product, update_product_data, update_user_password,
        update_restaurant_info
)

settings_bp = Blueprint('settings', __name__)


@settings_bp.route("/admin/settings/add", methods=["GET", "POST"])
@login_required("restaurant")
def add():
    """Add new product"""
    if request.method == "POST":
        product_data = get_product_data_from_request()
        product_image = get_product_image("image")
        product_image_cropped = get_product_image("image-cropped")

        validate_product_data(product_data)
        validate_product_image(product_image)

        add_new_product(product_data, product_image_cropped)

        flash("Added", "success")
        return redirect("/admin/settings/add")
    else:
        categories = Categories.query.filter_by(user_id=session.get("user_id"))
        return render_template("admin/settings/add.html",
                               categories=categories)


@settings_bp.route("/admin/settings/manage-categories", methods=["GET", "POST"])
@login_required("restaurant")
def manage_categories():
    """Manage categories"""
    restaurant_id = session.get("user_id")
    if request.method == "POST":
        form_fields = ["category"]

        data = get_data_from_form(form_fields)

        prevents_empty_fields(data)

        category = data["category"]

        search_category_name = Categories.query.filter_by(
                user_id=restaurant_id, category_name=category).first()

        if search_category_name:
            return abort(403, "the name of category already exists")

        new_category = Categories(category_name=category,
                                  user_id=restaurant_id)

        db.session.add(new_category)
        db.session.commit()

        return redirect("/admin/settings/manage-categories")

    categories = Categories.query.filter_by(user_id=restaurant_id)
    return render_template("admin/settings/manage-categories.html",
                           categories=categories)


@settings_bp.route("/admin/settings/manage-categories/delete", methods=["POST"])
@login_required("restaurant")
def delete_category():
    """Delete a category"""
    category_id = request.form.get("id")
    category = Categories.query.filter_by(id=category_id).first()
    products = Products.query.filter_by(category_id=category.id).all()

    if not products:
        db.session.delete(category)
        db.session.commit()

    else:
        return abort(403, "Need delete all products of this category before")

    return redirect("/admin/settings/manage-categories")


@settings_bp.route("/admin/settings/edit-menu")
@login_required("restaurant")
def edit_menu():
    """edit menu"""
    products = Products.query.filter_by(user_id=session.get("user_id")).all()
    return render_template("admin/settings/edit-menu.html",  products=products)


@settings_bp.route("/admin/settings/edit-menu/<product_id>", methods=["GET", "POST"])
@login_required("restaurant")
def edit_product(product_id):
    """edit a product of menu"""
    if request.method == "POST":
        product_data = get_product_data_from_request()

        update_product_data(product_data, product_id)

        flash("Edited", "success")
        return redirect(f"/admin/settings/edit-menu/{product_id}")

    user_id = session.get("user_id")

    product = Products.query.filter_by(user_id=user_id, id=product_id).first()

    if not product:
        return abort(403, "Choose a valid product")

    current_category = Categories.query.get(product.category_id)

    categories = Categories.query.filter(
            Categories.user_id == user_id,
            Categories.id != current_category.id).all()

    return render_template(
            "admin/settings/edit-menu-form.html", product=product,
            current_category=current_category, categories=categories)


@settings_bp.route("/admin/settings/edit-menu/<product_id>/delete", methods=["GET", "POST"])
@login_required("restaurant")
def delete_product(product_id):
    """edit a product of menu"""
    user_id = session.get("user_id")
    if request.method == "POST":
        product = Products.query.filter_by(
                id=product_id, user_id=user_id).first()

        if not product:
            return abort(403, "Choose a valid product")

        db.session.delete(product)
        db.session.commit()

        flash("Deleted", "success")
        return redirect("/admin/settings/edit-menu")

    return redirect("/admin/settings/edit-menu")


@settings_bp.route("/admin/settings/qr-code")
@login_required("restaurant")
def qr_code():
    """generate a qr code for restaurant"""
    restaurant_id = session.get("user_id")
    restaurant_data = RestaurantsData.query.filter_by(
            user_id=restaurant_id).first()

    restaurant_name = restaurant_data.name
    restaurant_url = restaurant_data.url

    return render_template("admin/settings/qr-code.html",
                           restaurant_name=restaurant_name,
                           restaurant_url=restaurant_url)


@settings_bp.route("/admin/settings/edit-restaurant-info", methods=["GET", "POST"])
@login_required("restaurant")
def edit_restaurant_info():
    """change user password"""
    restaurant_id = session.get("user_id")
    restaurant = RestaurantsData.query.filter_by(user_id=restaurant_id).first()

    if request.method == "POST":

        fields = ["name", "address", "phone", "url"]

        new_restaurant_info = get_data_from_form(fields)
        print(new_restaurant_info)

        prevents_empty_fields(new_restaurant_info)

        update_restaurant_info(restaurant_id, new_restaurant_info)

        flash("Changed", "success")
        return redirect("/admin/settings/edit-restaurant-info")

    return render_template("admin/settings/edit-restaurant-info.html",
                           restaurant=restaurant)


@settings_bp.route("/admin/settings/change-password", methods=["GET", "POST"])
@login_required("restaurant")
def change_password():
    """change user password"""
    if request.method == "POST":
        user_id = session.get("user_id")

        fields = ["current", "new", "confirm"]

        passwords = get_data_from_form(fields)

        validate_passwords(user_id, passwords)

        update_user_password(user_id, passwords["new"])

        flash("Changed", "success")
        return render_template("admin/settings/change-password.html")

    return render_template("admin/settings/change-password.html")


def init_app(app):
    """init admin settings blueprint"""
    app.register_blueprint(settings_bp)
