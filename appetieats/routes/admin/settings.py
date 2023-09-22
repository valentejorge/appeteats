from flask import (
        Blueprint, render_template, request, redirect, flash, session, abort
)
from appetieats.models import Categories, Products
from appetieats.ext.database import db

from appetieats.ext.helper.register_tools import login_required
from appetieats.ext.helper.get_inputs import (
        get_product_data_from_request, get_product_image
)
from appetieats.ext.helper.validate_inputs import (
        validate_product_data, validate_product_image
)
from appetieats.ext.helper.db_tools import add_new_product, update_product_data

settings_bp = Blueprint('settings', __name__)


@settings_bp.route("/admin/settings/add", methods=["GET", "POST"])
@login_required
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
@login_required
def manage_categories():
    """Manage categories"""
    if request.method == "POST":
        category = request.form.get("category", type=str)
        new_category = Categories(category_name=category,
                                  user_id=session.get("user_id"))

        db.session.add(new_category)
        db.session.commit()

        return redirect("/admin/settings/manage-categories")
    else:
        categories = Categories.query.filter_by(user_id=session.get("user_id"))
        return render_template("admin/settings/manage-categories.html",
                               categories=categories)


@settings_bp.route("/admin/settings/manage-categories/delete", methods=["POST"])
@login_required
def delete_category():
    """Delete a category"""
    id = request.form.get("id")
    category = Categories.query.filter_by(id=id).first()

    db.session.delete(category)
    db.session.commit()

    return redirect("/admin/settings/manage-categories")


@settings_bp.route("/admin/settings/edit-menu")
@login_required
def edit_menu():
    """edit menu"""
    products = Products.query.filter_by(user_id=session.get("user_id")).all()
    print(products)
    return render_template("admin/settings/edit-menu.html",  products=products)


@settings_bp.route("/admin/settings/edit-menu/<product_id>", methods=["GET", "POST"])
@login_required
def edit_product(product_id):
    """edit a product of menu"""
    if request.method == "POST":
        product_data = get_product_data_from_request()

        update_product_data(product_data, product_id)

        return redirect(f"/admin/settings/edit-menu/{product_id}")
    else:
        user_id = session.get("user_id")

        product = Products.query.filter_by(user_id=user_id,
                                           id=product_id).first()
        if not product:
            return abort(403, "Choose a valid product")

        current_category = Categories.query.filter_by(
                id=product.category_id).first()

        categories = Categories.query.filter(
                Categories.user_id == user_id,
                Categories.id != current_category.id).all()

        return render_template(
                "admin/settings/edit-menu-form.html", product=product,
                current_category=current_category, categories=categories)


def init_app(app):
    app.register_blueprint(settings_bp)
