import json

from backend.evaluator.analyzer import evaluate_answer


with open(
    "answer_output.json",
    "r",
    encoding="utf-8"
) as f:

    data=json.load(f)



answer=data["complete_answer"]


result=evaluate_answer(answer)


print("\n===================")
print("AI Evaluation")
print("===================")


print(json.dumps(
    result,
    indent=4
))