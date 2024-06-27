import logging
from concurrent.futures import ThreadPoolExecutor
from itertools import combinations
from core.hashing import a_hash, p_hash, g_hash, d_hash, calculate_similarity
from core.settings_handler import read_settings_from_json
from database.db import add_image_data, get_image_data, clear_database
from logger import logger


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


def process_hash_images_in_threads(image_paths, use_a_hash, use_p_hash, use_g_hash, use_d_hash, max_workers=10):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(process_hash_image, image_path, use_a_hash, use_p_hash, use_g_hash, use_d_hash) for
                   image_path in image_paths]
        for future in futures:
            try:
                future.result()
            except Exception as e:
                logging.error(f"Error in thread: {e}")


def find_hash(paths):
    use_a_hash = read_settings_from_json("aHash")
    use_g_hash = read_settings_from_json("gHash")
    use_p_hash = read_settings_from_json("pHash")
    use_d_hash = read_settings_from_json("dHash")
    process_hash_images_in_threads(paths, use_a_hash, use_p_hash, use_g_hash, use_d_hash)


def get_results_find_duplicates(image_paths_above, image_paths_below):
    threshold = read_settings_from_json("similarity_threshold")
    use_a_hash = read_settings_from_json("aHash")
    use_g_hash = read_settings_from_json("gHash")
    use_p_hash = read_settings_from_json("pHash")
    use_d_hash = read_settings_from_json("dHash")
    paths = None
    if image_paths_above and image_paths_below:
        paths = image_paths_above + image_paths_below
    elif image_paths_above:
        paths = image_paths_above
    elif image_paths_below:
        paths = image_paths_below

    clear_database()
    find_hash(paths)

    duplicates = []
    for path1, path2 in combinations(paths, 2):
        img1 = get_image_data(path1)
        img2 = get_image_data(path2)

        similarity = 0
        count = 0
        if use_a_hash:
            similarity += calculate_similarity(img1[2], img2[2])
            count += 1
        if use_g_hash:
            similarity += calculate_similarity(img1[3], img2[3])
            count += 1
        if use_p_hash:
            similarity += calculate_similarity(img1[4], img2[4])
            count += 1
        if use_d_hash:
            similarity += calculate_similarity(img1[5], img2[5])
            count += 1

        if count > 0:
            similarity /= count

        if similarity >= threshold:
            duplicates.append((img1[1], img2[1], similarity))

    results = {}
    for path1, path2, similarity in duplicates:
        if path1 not in results:
            results[path1] = {'similar_count': 0, 'similar_images': []}
        if path2 not in results:
            results[path2] = {'similar_count': 0, 'similar_images': []}

        results[path1]['similar_count'] += 1
        results[path1]['similar_images'].append({'path': path2, 'similarity': similarity})

        results[path2]['similar_count'] += 1
        results[path2]['similar_images'].append({'path': path1, 'similarity': similarity})

    results_list = []
    for path, data in results.items():
        results_list.append({
            'path': path,
            'similar_count': data['similar_count'],
            'similar_images': data['similar_images']
        })

    return results_list
