from django.http import HttpResponse, JsonResponse
from django.contrib.auth import get_user_model
from imagehistory.models import ImageHistory
import json

def home(request):
    return HttpResponse("Welcome to HabiScanAI Backend!")

def public_images(request):
    """Public endpoint to view all uploaded images (for testing purposes)"""
    images = ImageHistory.objects.all().order_by('-uploaded_at')
    data = {
        'count': images.count(),
        'results': []
    }
    
    for img in images:
        data['results'].append({
            'id': img.id,
            'user': img.user.email,
            'image': request.build_absolute_uri(img.image.url),
            'original_filename': img.original_filename,
            'content_hash': img.content_hash,
            'uploaded_at': img.uploaded_at.isoformat(),
        })
    
    return JsonResponse(data, json_dumps_params={'indent': 2})
