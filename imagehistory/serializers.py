from rest_framework import serializers
from .models import ImageHistory

class ImageHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageHistory
        fields = ['id', 'image', 'uploaded_at']