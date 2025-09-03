from rest_framework import serializers
from .models import ImageHistory

class ImageHistorySerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ImageHistory
        fields = ['id', 'user', 'image', 'uploaded_at', 'original_filename', 'content_hash']
        read_only_fields = ['uploaded_at', 'content_hash', 'user']