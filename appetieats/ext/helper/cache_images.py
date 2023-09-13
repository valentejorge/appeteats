import os
from appetieats.models import ProductImages


def get_image(image_name, image_id):
    CACHE_DIR = "appetieats/static/cache"
    cache_file_path = os.path.join(CACHE_DIR, image_name)

    if not os.path.exists(cache_file_path):
        image_data = ProductImages.query.get(image_id).image_data

        with open(cache_file_path, "wb") as file:
            file.write(image_data)
