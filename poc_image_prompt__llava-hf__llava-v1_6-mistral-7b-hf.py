#!/usr/bin/env python3
# ==========================================
# LLaVA Weather Forecast PoC
# Last experimented: 2025-11-19
# Platform: M1 Mac
# ==========================================

from transformers import AutoProcessor, AutoModelForVision2Seq
from PIL import Image
import torch

MODEL_NAME = "llava-hf/llava-v1.6-mistral-7b-hf"
MODEL_NAME = "Qwen/Qwen3-0.6B"

# Initialize processor and model
processor = AutoProcessor.from_pretrained(MODEL_NAME, use_fast=True)
model = AutoModelForVision2Seq.from_pretrained(MODEL_NAME)

# Load sample image
img = Image.open("sample.png")

# Prompt with special <image> token
prompt = "<image>\nUSER: Provide a short weather summary for Japan.\nASSISTANT:"

# Process input
print("=== PROCESS INPUT ===")
inputs = processor(text=prompt, images=img, return_tensors="pt")

# Generate output
print("=== GENERATE OUTPUT ===")
with torch.no_grad():
    out = model.generate(**inputs, max_new_tokens=150)

# Inspect raw output
print("=== RAW TENSOR ===")
print(out)
print("=== LIST FORM ===")
print(out.tolist())

# Decode output
decoded_clean = processor.decode(out[0], skip_special_tokens=True)
decoded_raw = processor.decode(out[0], skip_special_tokens=False)

print("=== DECODED RAW ===")
print(decoded_raw)
print("=== DECODED CLEAN ===")
print(decoded_clean)
