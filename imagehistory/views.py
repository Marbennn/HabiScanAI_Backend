from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from .models import ImageHistory
from .serializers import ImageHistorySerializer
import hashlib

class ImageHistoryViewSet(viewsets.ModelViewSet):
    queryset = ImageHistory.objects.all().order_by('-uploaded_at')
    serializer_class = ImageHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset().filter(user=self.request.user)
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

        hasher = hashlib.sha256()
        for chunk in file.chunks():
            hasher.update(chunk)
        content_hash = hasher.hexdigest()
        file.seek(0)

        existing = ImageHistory.objects.filter(user=request.user, content_hash=content_hash).first()
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
        instance = serializer.save(user=request.user)
        serializer = self.get_serializer(instance)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)