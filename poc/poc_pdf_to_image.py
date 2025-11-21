from pdf2image import convert_from_path

pages = convert_from_path("sample.pdf")
pages[0].save("sample.png")
print("Converted to sample.png")
