import cv2
import numpy as np


def preprocess_image(image_path, output_path=None):
    image = cv2.imread(image_path)

    if image is None:
        raise Exception(f"Image not found: {image_path}")

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Reduce noise while preserving handwriting
    gray = cv2.bilateralFilter(gray, 9, 75, 75)

    # Improve contrast
    gray = cv2.equalizeHist(gray)

    # Adaptive threshold
    binary = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        15
    )

    if output_path:
        cv2.imwrite(output_path, binary)

    return binary