import json

from backend.line_detector import detect_lines
from backend.ocr import extract_text
from backend.dataset_loader import load_model_answer
from backend.answer_comparator import compare_answers


def evaluate(image_path, question_id):
    print("Detecting lines...")

    line_images = detect_lines(image_path)

    print(f"Detected {len(line_images)} lines")

    student_answer = ""

    for line in line_images:
        text = extract_text(line)
        student_answer += text + " "

    student_answer = student_answer.strip()

    model = load_model_answer(question_id)

    result = compare_answers(
        model["question"],
        model["model_answer"],
        student_answer
    )

    result["student_answer"] = student_answer

    return result