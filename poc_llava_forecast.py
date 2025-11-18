from transformers import AutoProcessor, AutoModelForVision2Seq
from PIL import Image

proc = AutoProcessor.from_pretrained("llava-hf/llava-1.6-mistral-7b-hf")
model = AutoModelForVision2Seq.from_pretrained("llava-hf/llava-1.6-mistral-7b-hf")

img = Image.open("sample.png")

prompt = "Provide a short weather summary for Japan."
inputs = proc(prompt, img, return_tensors="pt")
out = model.generate(**inputs, max_new_tokens=150)

print(proc.decode(out[0], skip_special_tokens=True))
