#!/usr/bin/env python3
# ==========================================
# Qwen3-0.6B Weather Forecast PoC
# Last experimented: 2025-11-19
# Platform: M1 Mac
# ==========================================

from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

MODEL_NAME = "Qwen/Qwen3-0.6B"

# Load tokenizer and model (use float16 for speed on M1)
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, torch_dtype=torch.float16)

# Put model on CPU (M1 will use Metal automatically if available)
device = "mps" if torch.backends.mps.is_available() else "cpu"
model.to(device)

# Your prompt
prompt = "Provide a short weather summary for Japan."

# Tokenize input
inputs = tokenizer(prompt, return_tensors="pt").to(device)

# Generate output
with torch.no_grad():
    out = model.generate(**inputs, max_new_tokens=150)

# Decode and print
decoded = tokenizer.decode(out[0], skip_special_tokens=True)
print("=== Forecast ===")
print(decoded)

# Optional: see raw token IDs
print("=== Token IDs ===")
print(out.tolist())
