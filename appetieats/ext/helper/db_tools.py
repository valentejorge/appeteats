from appetieats.models import (
        Products, ProductImages, Orders, OrderItems, CustomersData
)
from werkzeug.utils import secure_filename
from appetieats.ext.database import db
from flask import session
import datetime


def add_new_product(product_data, product_image):
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

    return


def add_image(product_image, product_id):
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
    return


def update_product_data(product_data, id):
    product = Products.query.get(id)

    product.name = product_data["name"]
    product.description = product_data["description"]
    product.price = product_data["price"]
    product.barcode = product_data["barcode"]
    product.category_id = product_data["category"]

    db.session.commit()

    return


def add_new_oder(customer_id, restaurant_id, total_price, order_items):
    new_order = Orders(
            customer_id=customer_id,
            restaurant_id=restaurant_id,
            date=datetime.datetime.now().isoformat(),
            status="processing",
            total_price=total_price
    )
    db.session.add(new_order)
    db.session.commit()
    print(order_items)

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

    return


def get_orders(restaurant_id, status):
    orders = Orders.query.filter(
            Orders.restaurant_id == restaurant_id
            ).filter(
                    Orders.status == status
            ).order_by(
                    Orders.date.desc()
            ).all()
    return orders


def orders_to_dict(orders):
    order_data = []
    for order in orders:
        customer = CustomersData.query.filter(
                CustomersData.user_id == order.customer_id).first()
        order_dict = {
            "id": order.id,
            "customer_name": f"{customer.first_name} {customer.last_name}",
            "customer_address": f"{customer.address}, {customer.reference} - \
                                {customer.zip_code}",
            "customer_phone": {customer.phone},
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
