from PIL import Image
import numpy as np

from logger import logger


def resize_image_and_get_pixel_matrix(image_path, size):
    with Image.open(image_path) as img:
        img_resized = img.resize(size, Image.ANTIALIAS)
        pixel_matrix = np.array(img_resized)
    return pixel_matrix


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
