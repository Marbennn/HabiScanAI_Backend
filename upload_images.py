import os
import requests
import sys
import hashlib

folder_path = "pictures"
image_name = "test.jpg"

image_path = os.path.join(folder_path, image_name)
base_url = "http://127.0.0.1:8000"
url = f"{base_url}/api/history/images/"

# Prefer supplying a token via environment: set HABISCAN_TOKEN=... in your shell
TOKEN = os.getenv("HABISCAN_TOKEN", "")
# Optional: if TOKEN is empty and you want this script to fetch a token, set these:
USERNAME = os.getenv("HABISCAN_USERNAME", "")
PASSWORD = os.getenv("HABISCAN_PASSWORD", "")

def get_headers():
    headers = {}
    if TOKEN:
        headers["Authorization"] = f"Token {TOKEN}"
    return headers

def obtain_token(username: str, password: str) -> str:
    try:
        r = requests.post(
            f"{base_url}/api/auth/token/",
            json={"username": username, "password": password},
            timeout=10,
        )
        r.raise_for_status()
        data = r.json()
        return data.get("token", "")
    except Exception as e:
        print(f"Failed to obtain token: {e}")
        return ""

def sha256_of_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()

def main():
    global TOKEN
    if not os.path.exists(image_path):
        print(f"Image not found: {image_path}")
        sys.exit(1)

    file_hash = sha256_of_file(image_path)
    print(f"Hash: {file_hash}")

    # Ensure we have a token if the API requires authentication
    if not TOKEN and USERNAME and PASSWORD:
        TOKEN = obtain_token(USERNAME, PASSWORD)
        if TOKEN:
            print("Obtained token via credentials.")
        else:
            print("Warning: proceeding without token. Authenticated API calls may fail.")

    # Always POST - let the server handle deduplication
    try:
        with open(image_path, 'rb') as f:
            files = {'image': f}
            r = requests.post(url, files=files, headers=get_headers(), timeout=30)
        
        if r.status_code in (200, 201):
            item = r.json()
            if r.status_code == 200:
                print("✅ Image already exists in your history (deduplicated)")
            else:
                print("✅ New image uploaded to your history")
            
            print(f"  📋 ID: {item.get('id')}")
            print(f"  📁 File: {item.get('image')}")
            print(f"  📝 Original filename: {item.get('original_filename')}")
            print(f"  📅 Uploaded: {item.get('uploaded_at')}")
            print(f"  🔗 Hash: {item.get('content_hash')}")
        else:
            print(f"❌ Upload failed (status {r.status_code}): {r.text}")
    except Exception as e:
        print(f"❌ POST failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
