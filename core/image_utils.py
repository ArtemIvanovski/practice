from PIL import Image
import numpy as np
from logger import logger
import cv2


def dct_2d(image):
    """
    Performs a 2D Discrete Cosine Transform (DCT) on the given image.

    Parameters:
    image (np.ndarray): A 2D NumPy array representing the image. The shape of the array should be (height, width).

    Returns:
    np.ndarray: A 2D NumPy array representing the DCT of the input image. The shape of the array will be (height, width).

    Note:
    This function uses the cv2.dct function from the OpenCV library to perform the DCT.
    The input image should be a grayscale image represented as a 2D NumPy array.
    """
    return cv2.dct(np.float32(image))


def resize_image(image_path, new_width, new_height):
    """
    Resizes an image to the specified dimensions using the LANCZOS interpolation method.

    Parameters:
    image_path (str): The path to the image file.
    new_width (int): The new width of the image.
    new_height (int): The new height of the image.

    Returns:
    np.ndarray: A NumPy array representing the resized image.

    Raises:
    FileNotFoundError: If the image file is not found.
    IOError: If the image file is corrupted or cannot be opened.
    """
    image = Image.open(image_path)
    resized_image = image.resize((new_width, new_height), Image.LANCZOS)
    pixels = np.array(resized_image)
    return pixels


def convert_to_grayscale(pixels):
    """
    Converts a given RGB image to grayscale.

    Parameters:
    pixels (np.ndarray): A 3D NumPy array representing the RGB image. The shape of the array should be (height, width, 3).

    Returns:
    np.ndarray: A 2D NumPy array representing the grayscale image. The shape of the array will be (height, width).

    Raises:
    ValueError: If the input array does not have a shape of (height, width, 3).

    Note:
    The conversion to grayscale is performed be taking the mean of the RGB values along the third axis.
    """
    if len(pixels.shape) == 3 and pixels.shape[2] == 3:
        grayscale_pixels = np.mean(pixels, axis=2)
        return grayscale_pixels
    else:
        logger.error("Input matrix must be in RGB format")
        raise ValueError("Input matrix must be in RGB format")


def is_valid_image(image_path):
    """
    Checks if the given image file exists and can be opened without errors.

    Parameters:
    image_path (str): The path to the image file.

    Returns:
    bool: True if the image file is valid and can be opened, False otherwise.

    Raises:
    FileNotFoundError: If the image file is not found.
    IOError: If the image file is corrupted or cannot be opened.
    Exception: If an unknown error occurs during the processing of the image file.
    """
    try:
        Image.open(image_path)
        return True
    except FileNotFoundError:
        logger.error(f"Image '{image_path}' not found.")
        return False
    except IOError:
        logger.error(f"Failed to open image '{image_path}'. The image may be corrupted.")
        return False
    except Exception as e:
        logger.error(f"Unknown error occurred while processing file '{image_path}': {str(e)}")
        return False
