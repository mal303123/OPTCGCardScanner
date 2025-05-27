import cv2
import os
import numpy as np
import imagehash
from PIL import Image


hash_size = 16

def hash_image_from_array(read_img):
    PIL_img = Image.fromarray(read_img)
    dhash = imagehash.dhash(PIL_img, hash_size)
    phash = imagehash.phash(PIL_img, hash_size)

    dhash_bytes = dhash.hash.astype(np.uint8)
    phash_bytes = phash.hash.astype(np.uint8)

    # Concatenate the two hashes into one array
    combined_hash = np.concatenate([dhash_bytes, phash_bytes])
    packed = np.packbits(combined_hash).astype(np.uint8)
    return packed


##Debugging tools##

def print_hash_db(hash_db):
    # Print all items
    for name, hash_value in hash_db.items():
        print(f"{name}: {hash_value}")
    return

