## HabiScan Backend

Cross-platform backend (Web/Android/iOS) for scanning images and storing per-user history using Django REST Framework.

### 1) Project Structure

```bash
HabiScanAI_Backend/
├─ habiscan_backend/                  # Django project
├─ imagehistory/                      # Image history app (models, views, serializers)
├─ media/                             # Uploaded media files (served in DEV)
├─ pictures/                          # Test images
├─ manage.py                          # Django management
├─ requirements.txt                   # Python dependencies
└─ upload_images.py                   # Example client script
```

### 2) Setup

1. Create and activate virtual environment
```bash
python -m venv venv
```
```bash
venv\Scripts\activate.bat              # Windows
source venv/bin/activate               # macOS / Linux
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Configure environment (optional but recommended)
- In DEV, defaults work. For PROD set env vars:
  - `DEBUG=false`
  - `SECRET_KEY=<strong-secret>`
  - `ALLOWED_HOSTS=your.domain,localhost`
  - Configure media storage (S3/GCS) if not using local filesystem

4. Create and migrate database
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Create superuser (to log into admin and create users)
```bash
python manage.py createsuperuser
```

6. Run the development server
```bash
python manage.py runserver
```
- Server: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

### 3) Authentication (Token-based)

1. Obtain token
```bash
curl -X POST http://127.0.0.1:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"<your_user>", "password":"<your_pass>"}'
```
Response:
```json
{ "token": "<TOKEN>" }
```

2. Use token in subsequent requests
Add header: `Authorization: Token <TOKEN>`

### 4) Image History API

- List current user history
```bash
curl -H "Authorization: Token <TOKEN>" \
  http://127.0.0.1:8000/api/history/images/
```

- Upload new image (multipart form)
```bash
curl -H "Authorization: Token <TOKEN>" \
  -F image=@pictures/test_image.jpg \
  http://127.0.0.1:8000/api/history/images/
```
Notes:
- Deduplicated per-user by content hash. Re-uploading same image returns existing record.
- Query params: `?hash=<sha256>` and/or `?filename=<name>` to filter results.

### 5) Example Python client

Update `upload_images.py` to set your token and run:
```bash
python upload_images.py
```

### 6) File lifecycle & maintenance

- Deleting an image record removes the file from disk (DEV) or storage (PROD) automatically.
- Replacing an image file deletes the old file.
- Reconcile DB and filesystem:
```bash
python manage.py sync_images --dry-run
python manage.py sync_images --delete-unreferenced
```

### 7) Mobile/Web integration tips

- Store the user token securely (Keychain/Keystore/SecureStorage).
- Always send `Authorization: Token <TOKEN>`.
- Use pagination (page size 20) when listing history: `?page=1`.

### 8) Optional: CORS (for browser clients)

Install and enable if serving API to a separate web origin.
```bash
pip install django-cors-headers
```
Add to settings:
```python
INSTALLED_APPS += ['corsheaders']
MIDDLEWARE = ['corsheaders.middleware.CorsMiddleware'] + MIDDLEWARE
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
]
```
