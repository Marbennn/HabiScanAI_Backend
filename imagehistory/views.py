from rest_framework import viewsets
from .models import ImageHistory
from .serializers import ImageHistorySerializer

class ImageHistoryViewSet(viewsets.ModelViewSet):
    queryset = ImageHistory.objects.all()
    serializer_class = ImageHistorySerializer