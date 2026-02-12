# utils.py

"""
Utility functions for image processing and API interactions.
"""

import requests
from PIL import Image
import io


def fetch_image(url):
    """
    Fetch an image from a URL and return it as a PIL Image object.
    """
    response = requests.get(url)
    response.raise_for_status()
    image = Image.open(io.BytesIO(response.content))
    return image


def save_image(image, path):
    """
    Save a PIL Image object to the given path.
    """
    image.save(path)


def resize_image(image, size):
    """
    Resize a PIL Image object to the given size (width, height).
    """
    return image.resize(size)


def process_api_data(data):
    """
    Process data from an API response.
    Modify this function to suit the specific API interaction needs.
    """
    return data
