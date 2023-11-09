"""Module providing a tools for manipulate the database"""
import datetime
from flask import session
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
from flask_socketio import emit
from appetieats.ext.database import db
from appetieats.models import (
        Products, ProductImages, Orders, OrderItems, CustomersData, Users
)


def update_user_password(user_id, new_password):
    """update password of user"""
    user = Users.query.get(user_id)
    user.hash = generate_password_hash(new_password)

    db.session.commit()


def add_new_product(product_data, product_image):
    """add new product in database"""
    new_product = Products(
            name=product_data['name'],
            description=product_data['description'],
            price=product_data['price'].replace("$ ", ""),
            available="true",
            barcode=product_data["barcode"],
            user_id=session.get('user_id'),
            category_id=product_data['category']
    )
    db.session.add(new_product)
    db.session.commit()

    product_id = new_product.id

    add_image(product_image, product_id)


def add_image(product_image, product_id):
    """add product image in database"""
    image_name = secure_filename(
            f"product{product_id}.{product_image.filename.rsplit('.', 1)[1]}")

    image_data = product_image.read()

    new_image = ProductImages(
            product_id=product_id,
            image_path=image_name,
            image_data=image_data
    )
    db.session.add(new_image)
    db.session.commit()


def update_product_data(product_data, product_id):
    """update product data in database"""
    product = Products.query.get(product_id)

    product.name = product_data["name"]
    product.description = product_data["description"]
    product.price = product_data["price"]
    product.barcode = product_data["barcode"]
    product.category_id = product_data["category"]

    db.session.commit()


def add_new_order(customer_id, restaurant_id, total_price, order_items):
    """add a new order in database"""
    new_order = Orders(
            customer_id=customer_id,
            restaurant_id=restaurant_id,
            date=datetime.datetime.now().isoformat(),
            status="processing",
            total_price=total_price
    )
    db.session.add(new_order)
    db.session.commit()

    for item in order_items:
        new_item = OrderItems(
                order_id=new_order.id,
                product_id=item["id"],
                quantity=item["quantity"],
                item_price=item["price"],
                sub_total=item["sub_total"]
        )
        db.session.add(new_item)
        db.session.commit()

    order_emmit = orders_to_dict(get_order(new_order.id))

    emit("new_order", order_emmit, namespace="/dashboard", room=restaurant_id)


def get_order(order_id):
    """get a unique order from id"""
    order = Orders.query.filter(Orders.id == order_id).all()
    return order


def get_orders(restaurant_id, status):
    """get all orders from a restaurant with a specific status"""
    orders = Orders.query.filter(
            Orders.restaurant_id == restaurant_id
            ).filter(
                    Orders.status == status
            ).order_by(
                    Orders.date.asc()
            ).all()
    return orders


def orders_to_dict(orders):
    """put all orders into a dict"""
    order_data = []
    for order in orders:
        customer = CustomersData.query.filter(
                CustomersData.user_id == order.customer_id).first()
        order_dict = {
            "id": order.id,
            "customer_name": f"{customer.first_name} {customer.last_name}",
            "customer_address": f"{customer.address} - {customer.zip_code}",
            "customer_reference": customer.reference,
            "customer_phone": customer.phone,
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
    return order_data


def update_product_status(product, operation):
    """update status of product"""
    match product.status, operation:
        case "processing", "next":
            product.status = "cooking"

        case "cooking", "next":
            product.status = "done"

        case "cooking", "previous":
            product.status = "processing"

        case "done", "previous":
            product.status = "cooking"

    db.session.commit()
