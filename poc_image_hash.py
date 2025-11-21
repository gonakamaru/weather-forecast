import hashlib


def pdf_hash(path):
    """
    Calculate a SHA-256 hash of a PDF file.
    - Reads the file in small chunks (8 KB) so it works with large PDFs
      without loading the whole file into memory.
    - Returns a 64-character hex string fingerprint.
    """
    sha = hashlib.sha256()
    CHUNK_SIZE = 8192  # 8 KB per read

    with open(path, "rb") as f:
        while chunk := f.read(CHUNK_SIZE):
            sha.update(chunk)

    return sha.hexdigest()


hash_yesterday = pdf_hash("chart_yesterday.pdf")
hash_today = pdf_hash("chart_today.pdf")

print(f"yesterday: {hash_yesterday}")
print(f"today____: {hash_today}")
print(f"length: {len(hash_today)}")

if hash_yesterday == hash_today:
    print("No update")
else:
    print("Updated")
