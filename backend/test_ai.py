from backend.ai_evaluator import evaluate_answer
import json

answer = """
Globalization has increased economic growth.

It has also increased inequality.

Governments should balance development with inclusion.
"""

result = evaluate_answer(answer)

print(json.dumps(result, indent=4))