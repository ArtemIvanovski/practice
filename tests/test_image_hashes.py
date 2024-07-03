import numpy as np

from core.hashing import calculate_similarity, a_hash, p_hash, d_hash, g_hash, int32_to_binary_string, hamming_distance


def test_calculate_similarity():
    assert calculate_similarity(12345678, 87654321) == 73.4375
    assert calculate_similarity(62135488, 88484211) == 75
    assert calculate_similarity(12315455, 80815886) == 81.25
    assert calculate_similarity(45458484, 45458484) == 100.0


def test_a_hash():
    assert a_hash("assets/testImage.jpg") == 18444465626874441980


def test_p_hash():
    assert p_hash("assets/testImage.jpg") == np.int64(-1538587944350272951)


def test_d_hash():
    assert d_hash("assets/testImage.jpg") == 2616325417703162400


def test_g_hash():
    assert g_hash("assets/testImage.jpg") == 4611682550237101632


def test_int32_to_binary_string():
    assert int32_to_binary_string(12345678) == "0000000000000000000000000000000000000000101111000110000101001110"


def test_hamming_distance():
    assert hamming_distance("1010101010101010", "0101010101010101") == 16
