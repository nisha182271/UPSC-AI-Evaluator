import subprocess
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent

PADDLE_PYTHON = PROJECT_ROOT / "paddle_env" / "Scripts" / "python.exe"
OCR_WORKER = PROJECT_ROOT / "backend" / "paddle_ocr_worker.py"


def extract_text(image_path: str) -> str:

    command = [
        str(PADDLE_PYTHON),
        str(OCR_WORKER),
        str(Path(image_path).resolve())
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace"
    )

    if result.returncode != 0:
        error_message = result.stderr.strip()

        raise RuntimeError(
            f"PaddleOCR failed: {error_message}"
        )

    output = result.stdout

    start_marker = "===OCR_RESULT_START==="
    end_marker = "===OCR_RESULT_END==="

    if start_marker not in output or end_marker not in output:
        raise RuntimeError(
            "PaddleOCR did not return a valid OCR result."
        )

    text = output.split(start_marker, 1)[1]
    text = text.split(end_marker, 1)[0]
    text = text.strip()

    if len(text) < 20:
        raise RuntimeError(
            "PaddleOCR returned too little text to safely evaluate the answer."
        )

    print("\n==============================")
    print("PADDLEOCR TEXT")
    print("==============================")
    print(text)
    print("==============================")

    return text