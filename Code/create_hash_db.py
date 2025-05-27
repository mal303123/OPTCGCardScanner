import cv2
import os
import numpy as np
import imagehash
from PIL import Image
import pickle

hash_size = 16
hash_db = {}


def hash_image(read_img):
    PIL_img = Image.fromarray(read_img)
    dhash = imagehash.dhash(PIL_img, hash_size)
    phash = imagehash.phash(PIL_img, hash_size)

    dhash_bytes = dhash.hash.astype(np.uint8)
    phash_bytes = phash.hash.astype(np.uint8)

    # Concatenate the two hashes into one array
    combined_hash = np.concatenate([dhash_bytes, phash_bytes])
    packed = np.packbits(combined_hash).astype(np.uint8)
    return packed


def save_hash_db():
    # Save to file
    with open("hashes.pkl", "wb") as f:
        pickle.dump(hash_db, f)
    return


def update_hash_db(folder_path = "Cards"):
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            name = os.path.splitext(filename)[0]  # e.g., "card001"
            if name.lower().endswith("_small"):
                continue  # Skip any file ending with _small
            
            print("Hashing: ", name)
            path = os.path.join(root, filename)
            hash_result = hash_image_from_file(path)
            if hash_result is not None:
                hash_db[name] = hash_result

    save_hash_db()
    return hash_db

def hash_image_from_file(image_path):
    read_img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if read_img is None:
        print("Failed to read", image_path)
        return None
    return hash_image(read_img)




def print_hash_db():
    # Print all items
    for name, hash_value in hash_db.items():
        print(f"{name}: {hash_value}")
    return


def load_hash_db(pickle_path="hashes.pkl"):
    try:
        with open(pickle_path, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        print("Pickle file not found. Returning empty hash DB.")
        return {}




    # --- Webcam scanning ---
def capture_from_webcam():
    print("Opening Webcam...")
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Webcam not accessible.")
        return

    print("Press SPACE to capture an image, or ESC to exit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame.")
            break

        cv2.imshow("Scan Card", frame)
        key = cv2.waitKey(1)

        if key == 27:  # ESC
            break

        elif key == 32:  # SPACE
            # Pause and let user select ROI
            print("Draw a bounding box around the card.")
            roi = cv2.selectROI("Select Card", frame, showCrosshair=True)
            x, y, w, h = roi

            if w > 0 and h > 0: 
                cropped = frame[y:y+h, x:x+w]
                gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
                hash_from_cam = hash_image(gray)  # Use your defined function

                # Optional: match with existing hashes
                for name, ref_hash in hash_db.items():
                    dist = np.count_nonzero(hash_from_cam != ref_hash)
                    if dist < 55:    
                        print(f"Scanned card: {name}: {dist}")
            else:
                print("ROI not selected or canceled.")

    cap.release()
    cv2.destroyAllWindows()

#update_hash_db()
hash_db = load_hash_db()
# Start webcam capture
capture_from_webcam()
