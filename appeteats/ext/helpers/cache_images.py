"""Module to cache images from the database"""
import os
from appeteats.models import ProductImages
from flask import current_app


def get_image(image_name, image_id):
    """put a image from db into a cache dir"""
    # cache_dir_path = "appeteats/static/cache"
    cache_dir_path = current_app.config.get("CACHE_PATH")

    print(cache_dir_path)
    cache_file_path = os.path.join(cache_dir_path, image_name)

    if not os.path.exists(cache_file_path):
        image_data = ProductImages.query.filter(
                ProductImages.id == image_id).first().image_data

        with open(cache_file_path, "wb") as file:
            file.write(image_data)
