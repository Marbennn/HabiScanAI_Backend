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
