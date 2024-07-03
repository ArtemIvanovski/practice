import pytest
import numpy as np
from PIL import Image
from core.image_utils import resize_image, convert_to_grayscale, dct_2d, is_valid_image
import tempfile
import os


def create_test_image(width, height, color=(255, 0, 0)):
    """
    Creates a temporary image for testing.

    Parameters:
    width (int): The width of the image.
    height (int): The height of the image.
    color (tuple): The color of the image in RGB format.

    Returns:
    str: The path to the temporary image file.
    """
    image = Image.new("RGB", (width, height), color)
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    image.save(temp_file.name)
    return temp_file.name


def test_resize_image():
    image_path = create_test_image(100, 100)
    resized_image = resize_image(image_path, 50, 50)
    assert resized_image.shape == (50, 50, 3)
    os.remove(image_path)


def test_convert_to_grayscale():
    rgb_image = np.zeros((10, 10, 3), dtype=np.uint8)
    grayscale_image = convert_to_grayscale(rgb_image)
    assert grayscale_image.shape == (10, 10)
    assert np.array_equal(grayscale_image, np.zeros((10, 10)))
    with pytest.raises(ValueError):
        convert_to_grayscale(np.zeros((10, 10)))


def test_dct_2d():
    test_image = np.zeros((8, 8), dtype=np.float32)
    dct_image = dct_2d(test_image)
    assert dct_image.shape == (8, 8)


def test_is_valid_image():
    valid_image_path = create_test_image(10, 10)
    assert is_valid_image(valid_image_path) is True
    os.remove(valid_image_path)

    invalid_image_path = "non_existent_image.jpg"
    assert is_valid_image(invalid_image_path) is False

    corrupt_image_path = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg").name
    with open(corrupt_image_path, 'w') as f:
        f.write("not an image")
    assert is_valid_image(corrupt_image_path) is False
    os.remove(corrupt_image_path)
