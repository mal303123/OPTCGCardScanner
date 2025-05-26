import cv2
import os
import numpy as np
import imagehash
from PIL import Image
import pickle

hash_size = 16
hash_db = {}


def hash_image(image_path):
    read_img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if read_img is None:
        print("Failed to read", image_path)
    PIL_img = Image.fromarray(read_img)
    dhash = imagehash.dhash(PIL_img, hash_size)
    phash = imagehash.phash(PIL_img, hash_size)

    dhash_bytes = dhash.hash.astype(np.uint8)
    phash_bytes = phash.hash.astype(np.uint8)

    # Concatenate the two hashes into one array
    combined_hash = np.concatenate([dhash_bytes, phash_bytes])
    packed = np.packbits(combined_hash).astype(np.uint8)
    return packed

folder_path = "images/"
for filename in os.listdir(folder_path):
    if filename.endswith(".jpg"):
        name = filename[:-4]
        path = os.path.join(folder_path, filename)
        hash_db[name] = hash_image(path)

# Save to file
with open("hashes.pkl", "wb") as f:
    pickle.dump(hash_db, f)

# Print all items
for name, hash_value in hash_db.items():
    print(f"{name}: {hash_value}")
