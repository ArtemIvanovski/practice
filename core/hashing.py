from core.image_utils import resize_image, convert_to_grayscale, dct_2d
import numpy as np

from logger import logger


def a_hash(image_path):
    """
    Calculates the Average Hash (aHash) of an image.

    Parameters:
    image_path (str): The path to the image file.

    Returns:
    int: The Average Hash value of the image.

    The Average Hash is a perceptual image hashing algorithm that compares the average brightness of
    the image's 8x8 pixel blocks. It is a simple and efficient method for image similarity comparison.
    """
    pixels = resize_image(image_path, 8, 8)
    grayscale_pixels = convert_to_grayscale(pixels)
    avg = grayscale_pixels.mean()
    bits = (grayscale_pixels >= avg).flatten()
    hash_value = 0
    for bit in bits:
        hash_value = (hash_value << 1) | int(bit)

    return hash_value


def p_hash(image_path):
    """
    Calculates the Perceptual Hash (pHash) of an image.

    Parameters:
    image_path (str): The path to the image file.

    Returns:
    int: The Perceptual Hash value of the image.

    The Perceptual Hash is a perceptual image hashing algorithm that compares the Discrete Cosine Transform (DCT)
    coefficients of the image's 8x8 pixel blocks. It is a more complex and efficient method for image similarity comparison.
    """
    pixels = resize_image(image_path, 32, 32)
    grayscale_pixels = convert_to_grayscale(pixels)
    dct_transformed = dct_2d(grayscale_pixels)
    dct_reduced = dct_transformed[:8, :8]
    dct_flattened = dct_reduced.flatten()
    avg = np.mean(dct_flattened[1:])
    bits = (dct_flattened >= avg).astype(int)
    hash_value = 0
    for bit in bits:
        hash_value = (hash_value << 1) | bit

    return hash_value


def d_hash(image_path):
    """
    Calculates the Difference Hash (dHash) of an image.

    Parameters:
    image_path (str): The path to the image file.

    Returns:
    int: The Difference Hash value of the image.

    The Difference Hash is a perceptual image hashing algorithm that compares the pixel differences
    between adjacent 8x8 pixel blocks in a 9x8 grid. It is a simple and efficient method for image similarity comparison.
    """
    pixels = resize_image(image_path, 9, 8)
    grayscale_pixels = convert_to_grayscale(pixels)
    diff = grayscale_pixels[:, 1:] > grayscale_pixels[:, :-1]
    bits = diff.flatten()
    hash_value = 0
    for bit in bits:
        hash_value = (hash_value << 1) | int(bit)

    return hash_value


def g_hash(image_path):
    """
    Calculates the Gradient Hash (gHash) of an image.

    Parameters:
    image_path (str): The path to the image file.

    Returns:
    int: The Gradient Hash value of the image.

    The Gradient Hash is a perceptual image hashing algorithm that compares the pixel intensity differences
    between adjacent columns and rows in a 32x32 pixel grid. It is a simple and efficient method for image similarity comparison.
    The hash value is calculated be comparing the sum of pixel intensities in each column and row,
    and appending a '1' if the sum of the current column/row is greater than the next one, or a '0' otherwise.
    """
    pixels = resize_image(image_path, 32, 32)
    grayscale_pixels = convert_to_grayscale(pixels)
    rows, cols = grayscale_pixels.shape
    bits = []
    for col in range(cols - 1):
        col_sum = np.sum(grayscale_pixels[:, col])
        next_col_sum = np.sum(grayscale_pixels[:, col + 1])
        bits.append(1 if col_sum > next_col_sum else 0)
    for row in range(rows - 1):
        row_sum = np.sum(grayscale_pixels[row, :])
        next_row_sum = np.sum(grayscale_pixels[row + 1, :])
        bits.append(1 if row_sum > next_row_sum else 0)
    hash_value = 0
    for bit in bits:
        hash_value = (hash_value << 1) | bit

    return hash_value


def int32_to_binary_string(hash_int32, num_bits=64):
    """
    Converts a 32-bit integer hash value to a binary string.

    Parameters:
    hash_int32 (int): The 32-bit integer hash value.
    num_bits (int, optional): The number of bits to represent the hash value. Default is 64.

    Returns:
    str: The binary representation of the hash value, zero-padded to the specified number of bits.

    This function is used to convert a 32-bit integer hash value to a binary string,
    which can then be used for further processing or comparison.
    """
    hash_int = int(hash_int32)
    hash_binary = bin(hash_int & (2 ** num_bits - 1))[2:]
    hash_binary = hash_binary.zfill(num_bits)
    return hash_binary


def hamming_distance(hash1_bits, hash2_bits):
    """
    Calculates the Hamming distance between two binary hash values.

    Parameters:
    hash1_bits (str): The first binary hash value as a string.
    hash2_bits (str): The second binary hash value as a string.

    Returns:
    int: The Hamming distance between the two hash values.

    The Hamming distance is the number of positions at which the corresponding bits in two binary strings are different.
    This function checks if the lengths of the two hash values are equal. If not, it logs an error and raises a ValueError.
    Then, it iterates over the bits of the two hash values, comparing each pair of bits. If the bits are different,
    it increments the distance counter. Finally, it returns the calculated Hamming distance.
    """
    if len(hash1_bits) != len(hash2_bits):
        logger.error("Difference length between hash1 and hash")
        raise ValueError("Difference length between hash1 and hash")

    distance = 0
    for bit1, bit2 in zip(hash1_bits, hash2_bits):
        if bit1 != bit2:
            distance += 1

    return distance


def calculate_similarity(hash1, hash2, max_distance=64):
    """
    Calculates the similarity percentage between two hash values using the Hamming distance.

    Parameters:
    hash1 (int): The first hash value as a 32-bit integer.
    hash2 (int): The second hash value as a 32-bit integer.
    max_distance (int, optional): The maximum possible Hamming distance between two hash values. Default is 64.

    Returns:
    float: The similarity percentage between the two hash values. The value is calculated as (1 - distance / max_distance) * 100.

    The function first converts the hash values to binary strings using the int32_to_binary_string function.
    Then, it calculates the Hamming distance between the two binary strings using the hamming_distance function.
    Finally, it calculates the similarity percentage based on the Hamming distance and returns the result.
    """
    hash1 = int32_to_binary_string(int(hash1))
    hash2 = int32_to_binary_string(int(hash2))
    distance = hamming_distance(hash1, hash2)
    similarity_percent = (1 - distance / max_distance) * 100

    return similarity_percent
