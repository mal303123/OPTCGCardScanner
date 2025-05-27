import cv2
import os
import pickle
import utilities

hash_db = {}


def save_hash_db():
    # Save to file
    with open("hashes.pkl", "wb") as f:
        pickle.dump(hash_db, f)
    return


def create_hash_db(folder_path = "Cards"):
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            name = os.path.splitext(filename)[0]  # e.g., "card001"
            if name.lower().endswith("_small"):
                continue  # Skip any file ending with _small
            
            print("Hashing: ", name)
            path = os.path.join(root, filename)
            hash_result = hash_image_from_file_path(path)
            if hash_result is not None:
                hash_db[name] = hash_result

    save_hash_db()
    return hash_db


def hash_image_from_file_path(image_path):
    read_img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if read_img is None:
        print("Failed to read", image_path)
        return None
    return utilities.hash_image_from_array(read_img)

create_hash_db()

