import os
import requests
import sys

folder_path = "pictures"
image_name = "hotdog.jpg"

image_path = os.path.join(folder_path, image_name)
url = "http://127.0.0.1:8000/api/history/images/"

if not os.path.exists(folder_path):
    print(f"Folder not found: {folder_path}")
    sys.exit()
if not os.path.exists(image_path):
    print(f"Image not found: {image_path}")
    sys.exit()

try:
    with open(image_path, "rb") as f:
        files = {"image": f}
        response = requests.post(url, files=files)
    if response.status_code == 201:
        print(f"Uploaded successfully: {image_name}")
        print("Response:", response.json())
    else:
        print(f"Upload failed, Status code: {response.status_code}")
        print("Response:", response.text)
except Exception as e:
    print(f"Exception occurred: {e}")
