from pathlib import Path
import shutil
import time

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse

from backend.image_processing import preprocess_image
from backend.ocr import extract_text
from backend.ai_evaluator import evaluate_answer


app = FastAPI(title="UPSC AI Evaluator")

UPLOAD_DIR = Path("uploads")
PROCESSED_DIR = Path("processed")

UPLOAD_DIR.mkdir(exist_ok=True)
PROCESSED_DIR.mkdir(exist_ok=True)


@app.get("/")
def home():
    return {
        "message": "Welcome to UPSC AI Evaluator"
    }


@app.post("/upload")
async def upload_image(
    file: UploadFile = File(...)
):

    upload_path = UPLOAD_DIR / file.filename

    with upload_path.open("wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    processed_path = (
        PROCESSED_DIR / file.filename
    )

    # ------------------------------
    # IMAGE PREPROCESSING
    # ------------------------------

    start = time.time()

    try:

        preprocess_image(
            str(upload_path),
            str(processed_path)
        )

    except Exception as e:

        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "stage": "preprocessing",
                "message": str(e)
            }
        )

    preprocessing_time = (
        time.time() - start
    )

    print(
        f"Preprocessing : "
        f"{preprocessing_time:.2f} seconds"
    )

    # ------------------------------
    # OCR
    # ------------------------------

    start = time.time()

    try:

        """extracted_text = extract_text(
            str(processed_path)
        )"""
        extracted_text = extract_text(str(upload_path))

    except Exception as e:

        ocr_time = time.time() - start

        """print(
            f"Gemini OCR    : "
            f"{ocr_time:.2f} seconds"
        )"""
        print(f"PaddleOCR     : {ocr_time:.2f} seconds")

        return JSONResponse(
            status_code=503,
            content={
                "status": "ocr_unavailable",
                "stage": "ocr",
                "message": str(e),
                "uploaded_image": str(
                    upload_path
                ),
                "processed_image": str(
                    processed_path
                )
            }
        )

    ocr_time = time.time() - start

    print(
        f"Gemini OCR    : "
        f"{ocr_time:.2f} seconds"
    )

    # ------------------------------
    # STRICT AI EVALUATION
    # ------------------------------

    start = time.time()

    try:

        evaluation = evaluate_answer(
            extracted_text
        )

    except Exception as e:

        ollama_time = time.time() - start

        print(
            f"Ollama        : "
            f"{ollama_time:.2f} seconds"
        )

        return JSONResponse(
            status_code=500,
            content={
                "status": "evaluation_error",
                "stage": "ollama",
                "message": str(e),
                "extracted_text": extracted_text
            }
        )

    ollama_time = time.time() - start

    print(
        f"Ollama        : "
        f"{ollama_time:.2f} seconds"
    )

    # ------------------------------
    # TOTAL
    # ------------------------------

    total_time = (
        preprocessing_time
        + ocr_time
        + ollama_time
    )

    print("==============================")
    print(
        f"TOTAL         : "
        f"{total_time:.2f} seconds"
    )
    print("==============================")

    return {
        "status": "success",
        "uploaded_image": str(upload_path),
        "processed_image": str(processed_path),
        "extracted_text": extracted_text,
        "evaluation": evaluation
    }