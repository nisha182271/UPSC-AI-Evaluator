from transformers import TrOCRProcessor, VisionEncoderDecoderModel

print("Loading processor...")
processor = TrOCRProcessor.from_pretrained(
    "microsoft/trocr-large-handwritten",
    use_fast=False
)

print("Loading model...")
model = VisionEncoderDecoderModel.from_pretrained(
    "microsoft/trocr-large-handwritten"
)

print("✅ TrOCR loaded successfully!")

