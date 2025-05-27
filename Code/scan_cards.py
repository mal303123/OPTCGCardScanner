import utilities
import cv2
import pickle
import numpy as np


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

    x, y, w, h = 175, 35, 275, 380

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame.")
            break
        
        
        cropped = frame[y:y + h, x:x + w]
        cv2.imshow("Scan Card", cropped)
        key = cv2.waitKey(1)
        

        if key == 27:  # ESC
            break

        elif key == 32:  # SPACE
            # Pause and let user select ROI
            if w > 0 and h > 0: 
                gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
                hash_from_cam = utilities.hash_image_from_array(gray)  # Use your defined function
                # Optional: match with existing hashes
                lowest_dist = 58
                lowest_name = "unknown"  
                for name, ref_hash in hash_db.items():
                    dist = np.count_nonzero(hash_from_cam != ref_hash)
                    if dist < lowest_dist:
                        lowest_dist = dist
                        lowest_name = name    
                print(f"Scanned card: {lowest_name}: {lowest_dist}")        

    cap.release()
    cv2.destroyAllWindows()

hash_db = load_hash_db()
capture_from_webcam()