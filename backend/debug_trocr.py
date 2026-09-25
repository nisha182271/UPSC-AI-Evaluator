from transformers import TrOCRProcessor, VisionEncoderDecoderModel

print("Loading processor...")
processor = TrOCRProcessor.from_pretrained(
    "microsoft/trocr-base-handwritten",
    use_fast=False
)

print("Processor loaded successfully!")

print("Loading model...")
model = VisionEncoderDecoderModel.from_pretrained(
    "microsoft/trocr-base-handwritten"
)

print("✅ Model loaded successfully!")