import json

from backend.evaluate import evaluate

result = evaluate(
    image_path="uploads/image.jpeg",
    question_id="globalization"
)
print(json.dumps(result, indent=4))