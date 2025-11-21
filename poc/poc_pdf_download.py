import requests

URL = "https://www.data.jma.go.jp/yoho/data/wxchart/quick/ASAS_COLOR.pdf"

r = requests.get(URL)
open("sample.pdf", "wb").write(r.content)
print("Downloaded:", len(r.content), "bytes")
