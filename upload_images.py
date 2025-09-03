import os
import requests
import sys
import hashlib

folder_path = "pictures"
image_name = "haha.jpg"

image_path = os.path.join(folder_path, image_name)
url = "http://127.0.0.1:8000/api/history/images/"

def sha256_of_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()

def main():
    if not os.path.exists(image_path):
        print(f"Image not found: {image_path}")
        sys.exit(1)

    file_hash = sha256_of_file(image_path)
    print(f"Hash: {file_hash}")

    try:
        r = requests.get(url, params={'hash': file_hash}, timeout=10)
        r.raise_for_status()
    except Exception as e:
        print(f"GET failed: {e}")
        sys.exit(1)

    data = r.json()
    if isinstance(data, list) and len(data) > 0:
        item = data[0]
        print("Found existing image:")
        print(f"  id: {item.get('id')}")
        print(f"  image: {item.get('image')}")
        print(f"  uploaded_at: {item.get('uploaded_at')}")
        sys.exit(0)

    try:
        with open(image_path, 'rb') as f:
            files = {'image': f}
            r = requests.post(url, files=files, timeout=30)
        if r.status_code in (200, 201):
            item = r.json()
            if r.status_code == 200:
                print("Server says this image already exists (idempotent POST).")
            else:
                print("Uploaded new image.")
            print(f"  id: {item.get('id')}")
            print(f"  image: {item.get('image')}")
            print(f"  uploaded_at: {item.get('uploaded_at')}")
        else:
            print(f"Upload failed (status {r.status_code}): {r.text}")
    except Exception as e:
        print(f"POST failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()