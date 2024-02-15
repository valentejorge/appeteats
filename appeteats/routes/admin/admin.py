"""Module for admin routes"""
from flask import (
        Blueprint, render_template, session, jsonify, request, abort, redirect
)

from flask_socketio import emit

from appeteats.ext.helpers.register_tools import login_required
from appeteats.models import Orders
from appeteats.ext.helpers.db_tools import (
    get_orders, orders_to_dict, update_product_status
)

admin_bp = Blueprint('admin', __name__)


@admin_bp.route("/admin")
@login_required("restaurant")
def admin():
    """show admin page"""
    return render_template("admin/admin.html")


@admin_bp.route("/admin/dashboard", methods=["GET", "POST"])
@login_required("restaurant")
def dashboard():
    """show dashboard page"""
    status = None

    restaurant_id = session.get("user_id")

    if request.method == "POST":
        product_id = request.form.get("id", type=int)
        status = request.form.get("status", type=str)
        operation = request.form.get("operation", type=str)
        order = Orders.query.filter_by(id=product_id).filter_by(
                status=status).filter_by(restaurant_id=restaurant_id).first()
        if not order:
            abort(403, "Fatal Error: Product not found")

        print(order.customer_id)
        emit("update_customer_view",
             namespace="/customer", room=order.customer_id)
        update_product_status(order, operation)

    if status:
        return redirect(f"/admin/dashboard#{status}")

    return render_template("admin/dashboard.html")


@admin_bp.route("/admin/dashboard/data")
@login_required("restaurant")
def orders_data():
    """show orders data json"""
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
    return jsonify(order_data)


@admin_bp.route("/admin/settings")
@login_required("restaurant")
def settings():
    """show settings page"""
    return render_template("admin/settings.html")


def init_app(app):
    """init the admin blueprint"""
    app.register_blueprint(admin_bp)
