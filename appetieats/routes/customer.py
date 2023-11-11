"""Module for customer routes"""
from flask import (
        Blueprint, render_template, session, jsonify, request, flash, redirect
)
from appetieats.models import (
        Orders, OrderItems, Products, ProductImages, CustomersData
)
from appetieats.ext.helpers.register_tools import login_required
from appetieats.ext.helpers.get_inputs import get_data_from_form
from appetieats.ext.helpers.validate_inputs import (
        prevents_empty_fields, validate_passwords
)
from appetieats.ext.helpers.db_tools import (
        update_customer_info, update_user_password
)

customer_bp = Blueprint('customer', __name__)


@customer_bp.route("/customer")
@login_required("customer")
def index():
    """Show the landing page"""
    order_data = []

    user_id = session.get("user_id")

    # orders = Orders.query.filter(Orders.customer_id == user_id).all()
    orders = Orders.query.filter(Orders.customer_id == user_id).order_by(
            Orders.date.desc()).all()

    for order in orders:
        order_dict = {
            "id": order.id,
            "date": order.date,
            "status": order.status,
            "total_price": order.total_price,
            "items": []
        }

        order_items = OrderItems.query.filter(
                OrderItems.order_id == order.id).all()

        for item in order_items:
            products = Products.query.get(item.product_id)
            image = ProductImages.query.get(item.product_id)

            item_dict = {
                "product_name": products.name,
                "quantity": item.quantity,
                "item_price": item.item_price,
                "image_path": image.image_path,
                "sub_total": item.sub_total
            }

            order_dict["items"].append(item_dict)

        order_data.append(order_dict)

    for order in order_data:
        for item in order['items']:
            print(item)

    # return (jsonify(order_data))
    return render_template("customer/customer.html", order_data=order_data)


@customer_bp.route("/customer/data")
@login_required("customer")
def customer_data():
    """Return the data of customer"""
    order_data = []

    user_id = session.get("user_id")

    orders = Orders.query.filter(Orders.customer_id == user_id).order_by(
            Orders.date.desc()).all()

    for order in orders:
        order_dict = {
            "id": order.id,
            "date": order.date,
            "status": order.status,
            "total_price": order.total_price,
            "items": []
        }

        order_items = OrderItems.query.filter(
                OrderItems.order_id == order.id).all()

        for item in order_items:
            products = Products.query.get(item.product_id)
            image = ProductImages.query.get(item.product_id)

            item_dict = {
                "product_name": products.name,
                "quantity": item.quantity,
                "item_price": item.item_price,
                "image_path": image.image_path,
                "sub_total": item.sub_total
            }

            order_dict["items"].append(item_dict)

        order_data.append(order_dict)

    return jsonify(order_data)


@customer_bp.route("/customer/edit-customer-info", methods=["GET", "POST"])
@login_required("customer")
def edit_restaurant_info():
    """change customer infos"""
    customer_id = session.get("user_id")
    customer = CustomersData.query.filter_by(user_id=customer_id).first()

    if request.method == "POST":

        fields = ["first", "last", "phone", "address", "zip", "reference"]

        new_customer_info = get_data_from_form(fields)

        print(new_customer_info)

        prevents_empty_fields(new_customer_info)

        update_customer_info(customer_id, new_customer_info)

        flash("Changed", "success")
        return redirect("/customer/edit-customer-info")

    return render_template("customer/edit-customer-info.html",
                           customer=customer)


@customer_bp.route("/customer/change-password", methods=["GET", "POST"])
@login_required("customer")
def change_customer_password():
    """change customer password"""
    if request.method == "POST":
        user_id = session.get("user_id")

        fields = ["current", "new", "confirm"]

        passwords = get_data_from_form(fields)

        validate_passwords(user_id, passwords)

        update_user_password(user_id, passwords["new"])

        flash("Changed", "success")
        return render_template("customer/change-password.html")

    return render_template("customer/change-password.html")


def init_app(app):
    """int customer blueprint"""
    app.register_blueprint(customer_bp)
