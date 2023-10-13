from flask import Blueprint, render_template, session
from appetieats.models import Orders, OrderItems, Products, ProductImages
from appetieats.ext.helper.register_tools import login_required

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


def init_app(app):
    app.register_blueprint(customer_bp)
