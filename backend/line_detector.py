import cv2
import os
import numpy as np


def detect_lines(image_path, output_folder="lines"):

    os.makedirs(output_folder, exist_ok=True)

    image = cv2.imread(image_path)

    if image is None:
        raise Exception(f"Could not read image: {image_path}")

    # --------------------------------------------------
    # 1. Convert to grayscale
    # --------------------------------------------------
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # --------------------------------------------------
    # 2. Threshold handwriting
    # --------------------------------------------------
    binary = cv2.threshold(
        gray,
        0,
        255,
        cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )[1]

    # --------------------------------------------------
    # 3. Remove notebook horizontal ruling lines
    # --------------------------------------------------
    horizontal_kernel = cv2.getStructuringElement(
        cv2.MORPH_RECT,
        (80, 1)
    )

    horizontal_lines = cv2.morphologyEx(
        binary,
        cv2.MORPH_OPEN,
        horizontal_kernel
    )

    handwriting = cv2.subtract(
        binary,
        horizontal_lines
    )

    # --------------------------------------------------
    # 4. Connect characters belonging to the same line
    # --------------------------------------------------
    connect_kernel = cv2.getStructuringElement(
        cv2.MORPH_RECT,
        (25, 3)
    )

    connected = cv2.dilate(
        handwriting,
        connect_kernel,
        iterations=1
    )

    # --------------------------------------------------
    # 5. Horizontal projection
    # --------------------------------------------------
    projection = np.sum(connected > 0, axis=1)

    # Smooth projection
    smooth_kernel = np.ones(7) / 7

    projection = np.convolve(
        projection,
        smooth_kernel,
        mode="same"
    )

    # Dynamic threshold
    threshold = max(
        8,
        image.shape[1] * 0.005
    )

    active = projection > threshold

    # --------------------------------------------------
    # 6. Find text bands
    # --------------------------------------------------
    ranges = []
    start = None

    for y, value in enumerate(active):

        if value and start is None:
            start = y

        elif not value and start is not None:

            end = y

            if end - start >= 8:
                ranges.append((start, end))

            start = None

    if start is not None:
        ranges.append((start, image.shape[0]))

    # --------------------------------------------------
    # 7. Merge only very close bands
    # --------------------------------------------------
    merged = []

    for start, end in ranges:

        if not merged:
            merged.append([start, end])

        elif start - merged[-1][1] <= 8:
            merged[-1][1] = end

        else:
            merged.append([start, end])

    # --------------------------------------------------
    # 8. Remove old line images
    # --------------------------------------------------
    for file in os.listdir(output_folder):

        if file.startswith("line_") and file.endswith(".png"):

            os.remove(
                os.path.join(output_folder, file)
            )

    # --------------------------------------------------
    # 9. Save detected lines
    # --------------------------------------------------
    saved = []

    for i, (y1, y2) in enumerate(merged):

        padding = 12

        top = max(0, y1 - padding)
        bottom = min(
            image.shape[0],
            y2 + padding
        )

        crop = image[top:bottom, :]

        filename = os.path.join(
            output_folder,
            f"line_{i + 1:03d}.png"
        )

        cv2.imwrite(
            filename,
            crop
        )

        print(
            f"line_{i + 1:03d}.png -> "
            f"{crop.shape[1]} x {crop.shape[0]}"
        )

        saved.append(filename)

    print(
        f"\nDetected {len(saved)} lines"
    )

    return saved