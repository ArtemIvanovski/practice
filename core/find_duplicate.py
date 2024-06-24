import logging
from concurrent.futures import ThreadPoolExecutor

from core.hashing import a_hash, p_hash, g_hash, d_hash
from core.settings_handler import read_settings_from_json
from database.db import add_image_data
from logger import logger


def process_image(image_path, use_a_hash, use_p_hash, use_g_hash, use_d_hash):
    hash_a = hash_p = hash_g = hash_d = None
    try:
        if use_a_hash:
            hash_a = a_hash(image_path)
        if use_p_hash:
            hash_p = p_hash(image_path)
        if use_g_hash:
            hash_g = g_hash(image_path)
        if use_d_hash:
            hash_d = d_hash(image_path)
        add_image_data(image_path, hash_a, hash_p, hash_g, hash_d)
    except Exception as e:
        logger.error(f"Error processing {image_path}: {e}")


def process_images_in_threads(image_paths, use_a_hash, use_p_hash, use_g_hash, use_d_hash, max_workers=10):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(process_image, image_path, use_a_hash, use_p_hash, use_g_hash, use_d_hash) for image_path in image_paths]
        for future in futures:
            try:
                future.result()
            except Exception as e:
                logging.error(f"Error in thread: {e}")


def find_duplicate(image_paths_above, image_paths_below):
    use_a_hash = read_settings_from_json("aHash")
    use_g_hash = read_settings_from_json("gHash")
    use_p_hash = read_settings_from_json("pHash")
    use_d_hash = read_settings_from_json("dHash")
    if len(image_paths_below) == 0:
        paths = image_paths_above
    elif len(image_paths_above) == 0:
        paths = image_paths_below
    else:
        paths = image_paths_above + image_paths_below
    process_images_in_threads(paths, use_a_hash, use_p_hash, use_g_hash, use_d_hash)
