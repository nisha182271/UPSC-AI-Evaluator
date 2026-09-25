"""import sys
from paddleocr import PaddleOCR"""
import sys
from paddleocr import PaddleOCR

sys.stdout.reconfigure(encoding="utf-8")


def extract_text(image_path):
    ocr = PaddleOCR(lang="en")
    result = ocr.predict(image_path)

    texts = []

    for item in result:
        data = item.json

        if isinstance(data, str):
            import json
            data = json.loads(data)

        texts.extend(data["res"]["rec_texts"])

    return "\n".join(texts)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("ERROR: Image path is required.", file=sys.stderr)
        sys.exit(1)

    image_path = sys.argv[1]

    try:
        text = extract_text(image_path)

        print("===OCR_RESULT_START===")
        print(text)
        print("===OCR_RESULT_END===")
        #print(text, encoding="utf-8")

    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
    