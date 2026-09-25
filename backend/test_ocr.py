from backend.ocr import extract_text

IMAGE_PATH = r"C:\Users\Lenovo\OneDrive\Desktop\UPSC-AI-Evaluator\uploads\image.jpeg"

print("Running OCR on original image...")
print("Image:", IMAGE_PATH)

text = extract_text(IMAGE_PATH)

print("\n==============================")
print("DETECTED TEXT")
print("==============================")
print(text)
print("==============================")