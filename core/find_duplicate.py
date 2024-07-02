import logging
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from itertools import combinations
from core.hashing import a_hash, p_hash, g_hash, d_hash, calculate_similarity
from core.settings_handler import get_finder_settings
from database.db import add_image_data, get_image_data, clear_database
from logger import logger
from itertools import product


def process_hash_image(image_path, use_a_hash, use_p_hash, use_g_hash, use_d_hash):
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


def process_hash_images_in_threads(image_paths, use_a_hash, use_p_hash, use_g_hash, use_d_hash, max_workers=30):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(process_hash_image, image_path, use_a_hash, use_p_hash, use_g_hash, use_d_hash) for
                   image_path in image_paths]
        for future in futures:
            try:
                future.result()
            except Exception as e:
                logging.error(f"Error in thread: {e}")


def get_results_find_duplicates(image_paths_above, image_paths_below):
    threshold, use_a_hash, use_g_hash, use_p_hash, use_d_hash = get_finder_settings()

    paths = image_paths_above + image_paths_below if image_paths_above and image_paths_below else image_paths_above or image_paths_below

    clear_database()
    start_time_hash = time.time()
    process_hash_images_in_threads(paths, use_a_hash, use_p_hash, use_g_hash, use_d_hash)
    end_time_hash = time.time()
    hash_processing_time = end_time_hash - start_time_hash
    print(f"Time taken to process hash images: {hash_processing_time} seconds")
    start_time_total = time.time()
    duplicates = []

    if image_paths_above and image_paths_below:
        pairs_to_compare = product(image_paths_above, image_paths_below)
    else:
        pairs_to_compare = combinations(paths, 2)

    for path1, path2 in pairs_to_compare:
        similarity = compare_images(path1, path2, use_a_hash, use_g_hash, use_p_hash, use_d_hash)
        if similarity >= threshold:
            duplicates.append((path1, path2, similarity))

    results_list = aggregate_results(duplicates)
    end_time_total = time.time()
    total_time = end_time_total - start_time_total
    print(f"Total time taken to get results: {total_time} seconds")
    return results_list


def aggregate_results(duplicates):
    results = defaultdict(lambda: {'similar_count': 0, 'similar_images': []})

    for path1, path2, similarity in duplicates:
        results[path1]['similar_count'] += 1
        results[path1]['similar_images'].append({'path': path2, 'similarity': similarity})

        results[path2]['similar_count'] += 1
        results[path2]['similar_images'].append({'path': path1, 'similarity': similarity})

    results_list = [{'path': path, **data} for path, data in results.items()]
    return results_list


def compare_images(image_path1, image_path2, use_a_hash, use_g_hash, use_p_hash, use_d_hash):
    img1 = get_image_data(image_path1)
    img2 = get_image_data(image_path2)

    similarity = 0
    count = 0
    if use_a_hash:
        similarity += calculate_similarity(img1[2], img2[2])
        count += 1
    if use_g_hash:
        similarity += calculate_similarity(img1[4], img2[4])
        count += 1
    if use_p_hash:
        similarity += calculate_similarity(img1[3], img2[3])
        count += 1
    if use_d_hash:
        similarity += calculate_similarity(img1[5], img2[5])
        count += 1

    if count > 0:
        similarity /= count

    return similarity
