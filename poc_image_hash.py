import hashlib


def pdf_hash(path):
    sha = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(8192):
            sha.update(chunk)
    return sha.hexdigest()


hash_yesterday = pdf_hash("chart_yesterday.pdf")
hash_today = pdf_hash("chart_today.pdf")

if hash_yesterday == hash_today:
    print("No update")
else:
    print("Updated")
