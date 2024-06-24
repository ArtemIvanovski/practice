from core.image_utils import resize_image, convert_to_grayscale, dct_2d
import numpy as np

from logger import logger


def ahash(image_path, new_width, new_height):
    pixels = resize_image(image_path, new_width, new_height)
    grayscale_pixels = convert_to_grayscale(pixels)
    avg = grayscale_pixels.mean()
    bits = (grayscale_pixels >= avg).flatten()
    hash_value = 0
    for bit in bits:
        hash_value = (hash_value << 1) | int(bit)

    return hash_value


def phash(image_path):
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


def dhash(image_path):
    pixels = resize_image(image_path, 9, 8)
    grayscale_pixels = convert_to_grayscale(pixels)
    diff = grayscale_pixels[:, 1:] > grayscale_pixels[:, :-1]
    bits = diff.flatten()
    hash_value = 0
    for bit in bits:
        hash_value = (hash_value << 1) | int(bit)

    return hash_value


def ghash(image_path):
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
    hash_int = int(hash_int32)
    hash_binary = bin(hash_int & (2 ** num_bits - 1))[2:]
    hash_binary = hash_binary.zfill(num_bits)
    return hash_binary


def hamming_distance(hash1, hash2):
    hash1_bits = f"{hash1:#066b}"[2:]
    hash2_bits = f"{hash2:#066b}"[2:]

    if len(hash1_bits) != len(hash2_bits):
        logger.error("Difference length between hash1 and hash")
        raise ValueError("Хэши должны быть одинаковой длины")

    distance = 0
    for bit1, bit2 in zip(hash1_bits, hash2_bits):
        if bit1 != bit2:
            distance += 1

    return distance


def similarity_percentage(hash1, hash2, max_distance=64):
    hash1 = int32_to_binary_string(hash1)
    hash2 = int32_to_binary_string(hash2)
    distance = hamming_distance(hash1, hash2)
    similarity_percent = (1 - distance / max_distance) * 100

    return similarity_percent
