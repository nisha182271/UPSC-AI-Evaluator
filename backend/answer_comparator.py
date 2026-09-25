import json
import ollama
MODEL = "qwen2.5:3b"
def compare_answers(question, model_answer, student_answer):
    prompt = f"""
You are an expert UPSC examiner.
Question:
{question}
Official Model Answer:
{model_answer}
Student Answer:
{student_answer}
Compare the student's answer with the model answer.
Evaluate using:
Content (/30)
Structure (/20)
Analysis (/30)
Presentation (/20)
Return ONLY valid JSON in this format:
{{
    "scores": {{
        "content": 0,
        "structure": 0,
        "analysis": 0,
        "presentation": 0
    }},
    "total_marks": 0,
    "missing_points": [],
    "strong_points": [],
    "feedback": []
}}
"""
    response = ollama.chat(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    text = response["message"]["content"]

    return json.loads(text)