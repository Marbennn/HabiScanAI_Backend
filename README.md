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
├─ upload_images.py                   # Example upload script
└─ test_bulk_delete.py                # Interactive bulk delete script
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

1. Obtain token (PowerShell)
```powershell
$body = @{ username = "your_username"; password = "your_password" } | ConvertTo-Json
$response = Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/api/auth/token/" -ContentType "application/json" -Body $body
$token = $response.token
$env:HABISCAN_TOKEN = $token
```

2. Use token in subsequent requests
Add header: `Authorization: Token <TOKEN>`

### 4) Image History API

- List current user history (PowerShell)
```powershell
$token = $env:HABISCAN_TOKEN
Invoke-RestMethod -Method Get -Uri "http://127.0.0.1:8000/api/history/images/" -Headers @{ "Authorization" = "Token $token" }
```

- Upload new image (PowerShell)
```powershell
$token = $env:HABISCAN_TOKEN
Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/api/history/images/" -Headers @{ "Authorization" = "Token $token" } -Form @{ image = Get-Item ".\pictures\test_image.jpg" }
```

- Delete single image
```powershell
$token = $env:HABISCAN_TOKEN
Invoke-RestMethod -Method Delete -Uri "http://127.0.0.1:8000/api/history/images/123/" -Headers @{ "Authorization" = "Token $token" }
```

- Bulk delete multiple images
```powershell
$token = $env:HABISCAN_TOKEN
$body = @{ ids = @(1, 2, 3) } | ConvertTo-Json
Invoke-RestMethod -Method Delete -Uri "http://127.0.0.1:8000/api/history/images/bulk_delete/" -Headers @{ "Authorization" = "Token $token"; "Content-Type" = "application/json" } -Body $body
```

**Features:**
- ✅ Deduplicated per-user by content hash. Re-uploading same image returns existing record.
- ✅ Query params: `?hash=<sha256>` and/or `?filename=<name>` to filter results.
- ✅ Pagination: `?page=1` (20 items per page).
- ✅ Automatic file cleanup when deleting records.

### 5) Example Python Scripts

**Upload images:**
```bash
# Set token first
$env:HABISCAN_TOKEN = "your_token_here"

# Upload image
python upload_images.py
```

**Interactive bulk delete:**
```bash
# Set token first  
$env:HABISCAN_TOKEN = "your_token_here"

# Run interactive delete script
python test_bulk_delete.py
```
The bulk delete script will:
- Show all your images with numbered options
- Let you select which ones to delete (e.g., "1,3,5" or "all")
- Ask for confirmation before deleting
- Only delete what you selected

### 6) File Lifecycle & Maintenance

**Automatic cleanup:**
- ✅ Deleting an image record removes the file from disk automatically
- ✅ Replacing an image file deletes the old file
- ✅ Signals handle all file cleanup operations

**Manual maintenance:**
```bash
# Dry-run: see what would be cleaned up
python manage.py sync_images --dry-run

# Actually clean up orphaned files
python manage.py sync_images --delete-unreferenced
```

### 7) API Endpoints Summary

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/history/images/` | List user's images (paginated) |
| POST | `/api/history/images/` | Upload new image (deduplicated) |
| DELETE | `/api/history/images/{id}/` | Delete single image |
| DELETE | `/api/history/images/bulk_delete/` | Delete multiple images |
| POST | `/api/auth/token/` | Get authentication token |

### 8) Mobile/Web Integration Tips

- Store the user token securely (Keychain/Keystore/SecureStorage)
- Always send `Authorization: Token <TOKEN>` header
- Use pagination when listing history: `?page=1` (20 items per page)
- Handle deduplication: same image returns existing record with status 200
- Use bulk delete for better UX when removing multiple images

### 9) Optional: CORS (for browser clients)

Install and enable if serving API to a separate web origin:
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
