from transformers import AutoProcessor, AutoModelForVision2Seq
from PIL import Image
import torch

MODEL_NAME = "llava-hf/llava-interleave-qwen-0.5b-hf"
proc = AutoProcessor.from_pretrained(MODEL_NAME, use_fast=True)
model = AutoModelForVision2Seq.from_pretrained(MODEL_NAME)

# Load sample image
img = Image.open("sample.png").convert("RGB")

# Prompt describing what you want
prompt = (
    "Find Japan in this map. <image>"
)

# Process image and prompt together
inputs = proc(img, prompt, return_tensors="pt")

# Generate forecast
out = model.generate(
    **inputs,
    max_new_tokens=400,
    do_sample=True,
    top_p=0.9,
    temperature=0.7,
    pad_token_id=proc.tokenizer.eos_token_id
)

# Decode result
text_output = proc.decode(out[0], skip_special_tokens=True)

print("=== Forecast ===")
print(text_output)
