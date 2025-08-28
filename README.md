HabiScanAI_Backend/
├─ habiscan_backend/                  # Django project folder
│   ├─ __init__.py
│   ├─ asgi.py
│   ├─ settings.py
│   ├─ urls.py                        # Project URLs (includes admin, API, root path)
│   ├─ views.py                       # Home page view
│   └─ wsgi.py
│
├─ imagehistory/                      # Django app for image history
│   ├─ __init__.py
│   ├─ admin.py
│   ├─ apps.py
│   ├─ models.py                      # ImageHistory model
│   ├─ serializers.py                 # DRF serializer
│   ├─ urls.py                        # App URLs
│   └─ views.py                       # ImageHistory views
│
├─ media/                             # Uploaded media files (images)
│
├─ pictures/                          # Test images folder
│   └─ test_image.jpg                 # Example image to upload
│
├─ venv/                              # Python virtual environment
│
├─ db.sqlite3                         # SQLite database
├─ manage.py                          # Django management file
├─ upload_images.py                   # Script to upload images via API
└─ requirements.txt                   # Python dependencies

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