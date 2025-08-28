from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import ImageHistory
from .serializers import ImageHistorySerializer
import hashlib

class ImageHistoryViewSet(viewsets.ModelViewSet):
    queryset = ImageHistory.objects.all().order_by('-uploaded_at')
    serializer_class = ImageHistorySerializer

    def get_queryset(self):
        qs = super().get_queryset()
        h = self.request.query_params.get('hash')
        filename = self.request.query_params.get('filename')
        if h:
            qs = qs.filter(content_hash=h)
        if filename:
            qs = qs.filter(original_filename=filename)
        return qs

    def create(self, request, *args, **kwargs):
        file = request.FILES.get('image')
        if not file:
            return Response({'detail': 'No image uploaded.'}, status=status.HTTP_400_BAD_REQUEST)

        file_bytes = file.read()
        content_hash = hashlib.sha256(file_bytes).hexdigest()
        file.seek(0)

        existing = ImageHistory.objects.filter(content_hash=content_hash).first()
        if existing:
            serializer = self.get_serializer(existing)
            return Response(serializer.data, status=status.HTTP_200_OK)

        original_filename = file.name
        serializer = self.get_serializer(data={
            'image': file,
            'original_filename': original_filename,
            'content_hash': content_hash
        })
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)