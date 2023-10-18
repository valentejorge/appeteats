from flask import Blueprint, render_template, session, jsonify, request, abort

from appetieats.ext.helper.register_tools import login_required
from appetieats.models import Orders, OrderItems, Products, ProductImages
from appetieats.ext.helper.db_tools import (
    get_orders, orders_to_dict, update_product_status
)

admin_bp = Blueprint('admin', __name__)


@admin_bp.route("/admin")
@login_required("restaurant")
def admin():
    return render_template("admin/admin.html")


@admin_bp.route("/admin/dashboard", methods=["GET", "POST"])
@login_required("restaurant")
def dashboard():
    """show dashboard page"""
    if request.method == "POST":
        restaurant_id = session.get("user_id")
        id = request.form.get("id", type=int)
        status = request.form.get("status", type=str)
        operation = request.form.get("operation", type=str)
        product = Orders.query.filter_by(id=id).filter_by(
                status=status).filter_by(restaurant_id=restaurant_id).first()
        print(product)
        if not product:
            abort(403, "Fatal Error: Product not found")

        update_product_status(product, operation)

    order_data = {
            "processing": [],
            "cooking": [],
            "done": []
    }

    user_id = session.get("user_id")

    processing, cooking, done = (
            get_orders(user_id, "processing"),
            get_orders(user_id, "cooking"),
            get_orders(user_id, "done")
    )

    order_data["processing"], order_data["cooking"], order_data["done"] = (
            orders_to_dict(processing),
            orders_to_dict(cooking),
            orders_to_dict(done)
    )
    return render_template("admin/dashboard.html", order_data=order_data)


@admin_bp.route("/admin/dashboard/data")
@login_required("restaurant")
def orders_data():
    order_data = {
            "processing": [],
            "cooking": [],
            "done": []
    }

    user_id = session.get("user_id")

    processing, cooking, done = (
            get_orders(user_id, "processing"),
            get_orders(user_id, "cooking"),
            get_orders(user_id, "done")
    )

    order_data["processing"], order_data["cooking"], order_data["done"] = (
            orders_to_dict(processing),
            orders_to_dict(cooking),
            orders_to_dict(done)
    )
    print(order_data)
    return jsonify(order_data)


@admin_bp.route("/admin/settings")
@login_required("restaurant")
def settings():
    return render_template("admin/settings.html")


def init_app(app):
    app.register_blueprint(admin_bp)
