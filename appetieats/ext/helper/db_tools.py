from appetieats.models import Products, ProductImages
from werkzeug.utils import secure_filename
from appetieats.ext.database import db
from flask import session


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
