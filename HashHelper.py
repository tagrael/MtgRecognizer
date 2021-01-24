import cv2
import imagehash
import numpy


def hamming(one, two):
    return bin(int(one) ^ int(two)).count("1")


def dhash(image, hash_size=8):
    gray_scaled = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray_scaled, (hash_size + 1, hash_size))
    diff = resized[:, 1:] > resized[:, :-1]
    return sum([2 ** i for (i, v) in enumerate(diff.flatten()) if v])


def convert_hash(h):
    return int(numpy.array(h, dtype="float64"))


def compute_single_hash(image):
    result = imagehash.average_hash(image, hash_size=16)
    return convert_hash(int(str(result), base=16))
