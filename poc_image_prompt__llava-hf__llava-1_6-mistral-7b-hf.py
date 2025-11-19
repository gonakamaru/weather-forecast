from transformers import AutoProcessor, AutoModelForVision2Seq
from PIL import Image
import torch

MODEL_NAME = "llava-hf/llava-v1.6-mistral-7b-hf"

processor = AutoProcessor.from_pretrained(MODEL_NAME)
model = AutoModelForVision2Seq.from_pretrained(MODEL_NAME)

img = Image.open("sample.png")
prompt = "<image>\n Describe."

inputs = processor(text=prompt, images=img, return_tensors="pt")

with torch.no_grad():
    out = model.generate(**inputs, max_new_tokens=150)

print(processor.decode(out[0], skip_special_tokens=True))
