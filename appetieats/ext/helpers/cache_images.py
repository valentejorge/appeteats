"""Module to cache images from the database"""
import os
from appetieats.models import ProductImages


def get_image(image_name, image_id):
    """put a image from db into a cache dir"""
    cache_dir_path = "appetieats/static/cache"
    cache_file_path = os.path.join(cache_dir_path, image_name)

    if not os.path.exists(cache_file_path):
        image_data = ProductImages.query.get(image_id).image_data

        with open(cache_file_path, "wb") as file:
            file.write(image_data)
