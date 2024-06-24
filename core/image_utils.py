from PIL import Image
import numpy as np
from logger import logger
import cv2


def dct_2d(image):
    return cv2.dct(np.float32(image))


def resize_image(image_path, new_width, new_height):
    image = Image.open(image_path)
    resized_image = image.resize((new_width, new_height), Image.LANCZOS)
    pixels = np.array(resized_image)
    return pixels


def convert_to_grayscale(pixels):
    if len(pixels.shape) == 3 and pixels.shape[2] == 3:
        grayscale_pixels = np.mean(pixels, axis=2)
        return grayscale_pixels
    else:
        logger.error("Входная матрица должна быть в формате RGB")
        raise ValueError("Входная матрица должна быть в формате RGB")


def is_valid_image(image_path):
    try:
        Image.open(image_path)
        return True
    except FileNotFoundError:
        logger.error(f"Image '{image_path}' not find.")
        return False
    except IOError:
        logger.error(f"Не удалось открыть изображение '{image_path}'. Возможно, изображение повреждено.")
        return False
    except Exception as e:
        logger.error(f"Неизвестная ошибка при обработке файла '{image_path}': {str(e)}")
        return False
