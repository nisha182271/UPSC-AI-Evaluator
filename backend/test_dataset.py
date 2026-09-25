from backend.dataset_loader import load_model_answer

data = load_model_answer("globalization")

print(data["question"])
print()
print(data["model_answer"])
print()
print(data["keywords"])