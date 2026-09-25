from backend.line_detector import detect_lines

IMAGE_PATH = r"C:\Users\Lenovo\OneDrive\Desktop\UPSC-AI-Evaluator\uploads\image.jpeg"

lines = detect_lines(IMAGE_PATH)

print()
print("Detected", len(lines), "lines")

for line in lines:
    print(line)