from flask import request


def get_product_data_from_request():
    data = {}
    fields = {
            "name": str,
            "price": str,
            "description": str,
            "barcode": str,
            "category": str
    }
    for field, data_type in fields.items():
        data[field] = request.form.get(field, type=data_type)

    data["price"] = data["price"].replace("$ ", "")

    return data


def get_product_image(name):
    image = request.files[f"{name}"]
    return image
