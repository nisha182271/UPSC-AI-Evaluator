from .rubric import RUBRIC
def evaluate_answer(text):
    result = {}
    total_score = 0
    length = len(text.split())
    if length > 100:
        content_score = 30
    else:
        content_score = 15
    result["content"] = content_score
    if "introduction" in text.lower() or "conclusion" in text.lower():
        structure_score = 15
    else:
        structure_score = 8
    result["structure"] = structure_score
    if length > 200:
        analysis_score = 20
    else:
        analysis_score = 10
    result["analysis"] = analysis_score
    result["presentation"] = 10
    total_score = sum(result.values())
    return {
        "scores": result,
        "total_marks": total_score,
        "max_marks": 100,
        "feedback":
            generate_feedback(result)

    }



def generate_feedback(scores):

    feedback=[]


    if scores["content"] < 25:
        feedback.append(
            "Add more factual points and examples"
        )

    if scores["structure"] < 15:
        feedback.append(
            "Improve introduction and conclusion"
        )

    if scores["analysis"] < 15:
        feedback.append(
            "Add multidimensional analysis"
        )


    if not feedback:
        feedback.append(
            "Good answer structure"
        )


    return feedback