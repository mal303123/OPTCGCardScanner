import pytesseract
import numpy as np
import cv2
from PIL import Image


block_custom_config = r'--oem 3 --psm 7 -c tessedit_char_whitelist=1234567890'
rarity_custom_config = r'--oem 3 --psm 7 -c tessedit_char_whitelist=LSRECU'
code_custom_config = r'--oem 3 --psm 7 -c tessedit_char_whitelist=OP0123456789STEB-'
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

img_name = "OP05-091"

rarity_section_y_start, rarity_section_y_end, rarity_section_x_start, rarity_section_x_end = 780, 810, 520, 550
block_section_y_start, block_section_y_end, block_section_x_start, block_section_x_end = 780, 815, 540, 570
code_section_y_start, code_section_y_end, code_section_x_start, code_section_x_end = 775, 820, 445, 525


def image_to_greyscale(input_img):

    input_img = cv2.imread(rf"images/" + img_name + ".jpg")
    gray = cv2.cvtColor(input_img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)

    return thresh




def clean_crop_background(crop):
    # Invert so dark background becomes white, white text box becomes black

    h, w = crop.shape
    mask = np.zeros((h + 2, w + 2), np.uint8)

    # Seeds as (x, y) = (col, row), corrected from original (row, col)
    seeds = [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)]

    for seed in seeds:
            cv2.floodFill(crop, mask, seedPoint=seed, newVal=255, loDiff=10, upDiff=10)
    
    return crop


def scan_card():
    
    thresh = image_to_greyscale(img_name)
    thresh_inv = cv2.bitwise_not(thresh)

    rarity_raw = thresh[780:810, 520:550] 
    block_raw = thresh[780:815, 540:570]
    code_raw = thresh_inv[775:820, 445:525]

    rarity_clean = clean_crop_background(rarity_raw)
    block_clean = clean_crop_background(block_raw)
    code_clean = clean_crop_background(code_raw)

    rarity_final = cv2.resize(rarity_clean, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    block_final = cv2.resize(block_clean, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    code_final = cv2.resize(code_clean, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    rarity_text = pytesseract.image_to_string(rarity_final, config = rarity_custom_config)
    block_text = pytesseract.image_to_string(block_final, config = block_custom_config)
    code_text = pytesseract.image_to_string(code_final, config = code_custom_config)

    print("Rarity: " + rarity_text)
    print("Block: " + block_text)
    print("Card: " + code_text)

    return

def scan_card(y_start, y_end, x_start, x_end, img_name):
    
    thresh = image_to_greyscale(img_name)
    thresh_inv = cv2.bitwise_not(thresh)

    section_raw = thresh[y_start:y_end, x_start:x_end] 
    
    section_clean = clean_crop_background(section_raw)

    section_final = cv2.resize(section_clean, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    section_text = pytesseract.image_to_string(section_final, config = rarity_custom_config)

    return(section_text)


cv2.waitKey(0)
cv2.destroyAllWindows()


"""    cv2.imshow('code', code_final)
    cv2.imshow('rarity', rarity_final)
    cv2.imshow('block', block_final)"""