HabiScanAI-Backend/
├─ habiscan_backend/              # Django project settings
│   ├─ __init__.py
│   ├─ settings.py                # Django settings
│   ├─ urls.py                    # URL configuration
│   ├─ asgi.py
│   └─ wsgi.py
│
├─ imagehistory/                  # Django app for Image History
│   ├─ __init__.py
│   ├─ admin.py
│   ├─ apps.py
│   ├─ models.py                  # Image model
│   ├─ serializers.py             # DRF serializers
│   ├─ views.py                   # Upload & Home views
│   ├─ urls.py                    # App-specific URLs
│   └─ migrations/                
│       └─ __init__.py
│
├─ media/                         # Uploaded images will be stored here
│   └─ images/                    
│       └─ (uploaded files)
│
├─ pictures/                      # Test images for upload
│   └─ test_image.jpg             
│
├─ venv/                          # Python virtual environment
│   └─ (env files)
│
├─ db.sqlite3                      # SQLite database
├─ manage.py                       # Django management script
├─ test_upload.py                  # Test script for single image upload
└─ upload_images.py                # Single-image uploader from pictures folder

1. Create and activate virtual environment
- python -m venv venv

- venv\Scripts\activate.bat              # Windows
- source venv/bin/activate               # macOS / Linux

2. Install dependencies
pip install -r requirements.txt

3. Apply migrations
- python manage.py makemigrations
- python manage.py migrate

4. Run the development server
- python manage.py runserver
Server runs at: http://127.0.0.1:8000/
API for image history: http://127.0.0.1:8000/api/history/images/

5. Upload Test Images
Place your test images in the pictures/ folder.
Run the single image uploader:
- python upload_images.py
Check uploaded images in media/images/ or via API:

Scripts
test_upload.py → Basic test script to upload a single image.
upload_images.py → Uploads a single image from the pictures/ folder.
