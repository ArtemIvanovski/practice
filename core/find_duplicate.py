import logging
from concurrent.futures import ThreadPoolExecutor

from database.db import add_image_data
from logger import logger
from hashing import a_hash, p_hash, g_hash, d_hash


def process_image(image_path):
    try:
        hash_a = a_hash(image_path)
        hash_p = p_hash(image_path)
        hash_g = g_hash(image_path)
        hash_d = d_hash(image_path)
        add_image_data(image_path, hash_a, hash_p, hash_g, hash_d)
    except Exception as e:
        logger.error(f"Error processing {image_path}: {e}")


def process_images_in_threads(image_paths, max_workers=10):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(process_image, image_path) for image_path in image_paths]
        for future in futures:
            try:
                future.result()
            except Exception as e:
                logging.error(f"Error in thread: {e}")


def find_duplicate(image_paths_above, image_paths_below):
    if len(image_paths_below) == 0:
        paths = image_paths_above
    elif len(image_paths_above) == 0:
        paths = image_paths_below
    else:
        paths = image_paths_above + image_paths_below
    process_images_in_threads(paths)
