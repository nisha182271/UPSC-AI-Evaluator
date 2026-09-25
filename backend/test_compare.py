from backend.dataset_loader import load_model_answer
from backend.answer_comparator import compare_answers
import json

data = load_model_answer("globalization")

student_answer = """
Globalization has increased economic growth,
trade and employment.

It has also increased inequality.

Government should ensure inclusive development.
"""

result = compare_answers(
    data["question"],
    data["model_answer"],
    student_answer
)

print(json.dumps(result, indent=4))