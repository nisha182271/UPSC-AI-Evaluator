import json
from pathlib import Path


def load_model_answer(topic):
    path = Path("dataset") / "gs3" / f"{topic}.json"

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)