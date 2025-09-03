from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
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

        # Calculate hash
        hasher = hashlib.sha256()
        for chunk in file.chunks():
            hasher.update(chunk)
        content_hash = hasher.hexdigest()
        file.seek(0)

        # Check if this exact image already exists for this user
        existing = ImageHistory.objects.filter(user=request.user, content_hash=content_hash).first()
        if existing:
            # Return existing record with 200 status
            serializer = self.get_serializer(existing)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # Create new record
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

    @action(detail=False, methods=['delete'])
    def bulk_delete(self, request):
        """
        Delete multiple images by providing a list of IDs.
        POST /api/history/images/bulk_delete/ with body: {"ids": [1, 2, 3]}
        """
        ids = request.data.get('ids', [])
        if not ids:
            return Response(
                {'detail': 'No IDs provided. Send {"ids": [1, 2, 3]}'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not isinstance(ids, list):
            return Response(
                {'detail': 'IDs must be a list of integers'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Filter to only user's images and existing IDs
        user_images = self.get_queryset().filter(id__in=ids)
        deleted_count = user_images.count()
        
        if deleted_count == 0:
            return Response(
                {'detail': 'No images found with the provided IDs'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Delete the images (signals will handle file cleanup)
        user_images.delete()
        
        return Response({
            'detail': f'Successfully deleted {deleted_count} image(s)',
            'deleted_count': deleted_count,
            'deleted_ids': list(user_images.values_list('id', flat=True))
        }, status=status.HTTP_200_OK)