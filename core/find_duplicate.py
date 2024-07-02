import logging
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from itertools import combinations
from core.hashing import a_hash, p_hash, g_hash, d_hash, calculate_similarity
from core.settings_handler import get_finder_settings
from database.db import add_image_data, get_image_data, clear_database
from logger import logger
from itertools import product


def process_hash_image(image_path, use_a_hash, use_p_hash, use_g_hash, use_d_hash):
    """
    Processes an image file to calculate hash values for different algorithms (a_hash, p_hash, g_hash, d_hash)
    and stores the results in the database.

    Parameters:
    image_path (str): The path to the image file.
    use_a_hash (bool): A flag indicating whether to calculate a_hash.
    use_p_hash (bool): A flag indicating whether to calculate p_hash.
    use_g_hash (bool): A flag indicating whether to calculate g_hash.
    use_d_hash (bool): A flag indicating whether to calculate d_hash.

    Returns:
    None

    Raises:
    Exception: If any error occurs during the image processing or database insertion.
    """
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
    """
    Processes a list of image files in parallel using multiple threads to calculate hash values for different algorithms
    (a_hash, p_hash, g_hash, d_hash) and stores the results in the database.

    Parameters:
    image_paths (list): A list of paths to the image files.
    use_a_hash (bool): A flag indicating whether to calculate a_hash.
    use_p_hash (bool): A flag indicating whether to calculate p_hash.
    use_g_hash (bool): A flag indicating whether to calculate g_hash.
    use_d_hash (bool): A flag indicating whether to calculate d_hash.
    max_workers (int, optional): The maximum number of threads to use for processing. Defaults to 30.

    Returns:
    None

    Raises:
    Exception: If any error occurs during the image processing or database insertion in a thread.
    """
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(process_hash_image, image_path, use_a_hash, use_p_hash, use_g_hash, use_d_hash) for
                   image_path in image_paths]
        for future in futures:
            try:
                future.result()
            except Exception as e:
                logging.error(f"Error in thread: {e}")


def get_results_find_duplicates(image_paths_above, image_paths_below):
    """
    This function finds duplicate images in two sets of image paths. It uses hash values to compare images and
    returns a list of dictionaries containing the duplicate image pairs and their similarity scores.

    Parameters:
    image_paths_above (list): A list of paths to the first set of image files.
    image_paths_below (list): A list of paths to the second set of image files.

    Returns:
    list: A list of dictionaries, where each dictionary represents a duplicate image pair and contains the following keys:
          - 'path1' (str): The path of the first image file.
          - 'path2' (str): The path of the second image file.
          - 'similarity' (float): The similarity score between the two images.
    """
    threshold, use_a_hash, use_g_hash, use_p_hash, use_d_hash = get_finder_settings()

    paths = image_paths_above + image_paths_below if image_paths_above and image_paths_below else image_paths_above or image_paths_below

    clear_database()

    process_hash_images_in_threads(paths, use_a_hash, use_p_hash, use_g_hash, use_d_hash)

    duplicates = []

    if image_paths_above and image_paths_below:
        pairs_to_compare = product(image_paths_above, image_paths_below)
    else:
        pairs_to_compare = combinations(paths, 2)

    def process_pair(pair):
        path1, path2 = pair
        similarity = compare_images(path1, path2, use_a_hash, use_g_hash, use_p_hash, use_d_hash)
        if similarity >= threshold:
            return (path1, path2, similarity)
        return None

    with ThreadPoolExecutor(max_workers=30) as executor:
        future_to_pair = {executor.submit(process_pair, pair): pair for pair in pairs_to_compare}
        for future in as_completed(future_to_pair):
            result = future.result()
            if result:
                duplicates.append(result)

    results_list = aggregate_results(duplicates)
    return results_list


def aggregate_results(duplicates):
    """
    Aggregates the duplicate image results and returns a list of dictionaries.

    Parameters:
    duplicates (list): A list of tuples, where each tuple contains three elements:
                      - path1 (str): The path of the first image file.
                      - path2 (str): The path of the second image file.
                      - similarity (float): The similarity score between the two images.

    Returns:
    list: A list of dictionaries, where each dictionary represents an image file and contains the following keys:
          - 'path' (str): The path of the image file.
          - 'similar_count' (int): The number of duplicate images found for this image.
          - 'similar_images' (list): A list of dictionaries, where each dictionary represents a duplicate image and contains the following keys:
                                     - 'path' (str): The path of the duplicate image.
                                     - 'similarity' (float): The similarity score between the original image and the duplicate image.
    """
    results = defaultdict(lambda: {'similar_count': 0, 'similar_images': []})

    for path1, path2, similarity in duplicates:
        results[path1]['similar_count'] += 1
        results[path1]['similar_images'].append({'path': path2, 'similarity': similarity})

        results[path2]['similar_count'] += 1
        results[path2]['similar_images'].append({'path': path1, 'similarity': similarity})

    results_list = [{'path': path, **data} for path, data in results.items()]
    return results_list


def compare_images(image_path1, image_path2, use_a_hash, use_g_hash, use_p_hash, use_d_hash):
    """
    Compares two images based on their hash values and returns the similarity score.

    Parameters:
    image_path1 (str): The path to the first image file.
    image_path2 (str): The path to the second image file.
    use_a_hash (bool): A flag indicating whether to use a_hash for comparison.
    use_g_hash (bool): A flag indicating whether to use g_hash for comparison.
    use_p_hash (bool): A flag indicating whether to use p_hash for comparison.
    use_d_hash (bool): A flag indicating whether to use d_hash for comparison.

    Returns:
    float: The similarity score between the two images, ranging from 0 (no similarity) to 100 (identical).
    """
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
