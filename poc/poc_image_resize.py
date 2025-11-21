from PIL import Image
import os

SRC_PATH = "sample.png"
DST_PATH = "sample_small.png"
WIDTH = 300

img = Image.open(SRC_PATH)
w, h = img.size
ratio = WIDTH / float(w)
new_size = (WIDTH, int(h * ratio))

img = img.resize(new_size, Image.LANCZOS)  # Use LANCZOS for high-quality downsampling
img.save(DST_PATH, optimize=True)

print(f"Resized: {SRC_PATH} -> {DST_PATH}")
print(f"Original: {os.path.getsize(SRC_PATH)} bytes")
print(f"Resized : {os.path.getsize(DST_PATH)} bytes")
