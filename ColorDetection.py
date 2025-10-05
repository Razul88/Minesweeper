import numpy as np
import cv2
import glob
import os

def load_templates(template_dir="numbers_templates"):
    """Load digit numbers_templates (1-8) from a directory."""
    templates = {}
    for path in glob.glob(os.path.join(template_dir, "*.png")):
        digit = os.path.splitext(os.path.basename(path))[0]  # filename = "1.png"
        if digit == "0":
            continue  # skip 0 template
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        templates[digit] = img
    return templates


def is_empty_cell(cell_img, bg_colors, uniform_threshold=0.95, tolerance=30):
    """
    Return True if cell is empty (0) based on two criteria:
    1. The cell is mostly uniform in color (high uniformity).
    2. The uniform color matches one of the background colors.
    """
    # Convert to NumPy array if it's PIL Image
    if not isinstance(cell_img, np.ndarray):
        cell_img = np.array(cell_img)

    # If grayscale, convert to 3 channels for color comparison
    if len(cell_img.shape) == 2:
        cell_img = cv2.cvtColor(cell_img, cv2.COLOR_GRAY2BGR)

    # Compute the most common color in the cell
    pixels = cell_img.reshape(-1, 3)
    median_color = np.median(pixels, axis=0)

    # Check uniformity
    diff = np.linalg.norm(pixels - median_color, axis=1)
    uniform_ratio = np.mean(diff < 10)  # pixels close to median
    if uniform_ratio < uniform_threshold:
        return False  # not uniform enough → probably contains number

    for bg in bg_colors:
        diff = np.abs(cell_img.astype(int) - np.array(bg))
        if np.mean(diff) < tolerance:
            return True
    return False

def detect_digit_in_cell(cell_img, bg_colors, templates, match_threshold=0.8) -> int | None:
    """Detect the digit in a single cell image. Returns digit as str or None."""
    # First, check if the cell is empty
    if is_empty_cell(cell_img, bg_colors):
        return 0

    if len(cell_img.shape) == 3:
        gray_cell = cv2.cvtColor(cell_img, cv2.COLOR_BGR2GRAY)
    else:
        gray_cell = cell_img

    best_digit = None
    best_conf = 0

    for digit, template in templates.items():
        w, h = template.shape[::-1]
        if gray_cell.shape[0] < h or gray_cell.shape[1] < w:
            continue  # skip if template is larger than cell
        res = cv2.matchTemplate(gray_cell, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        if max_val >= match_threshold and max_val > best_conf:
            best_conf = max_val
            best_digit = int(digit)
    return best_digit  # returns None if no digit detected