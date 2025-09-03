from django.db import models
from django.contrib.auth import get_user_model

class ImageHistory(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='image_histories')
    image = models.ImageField(upload_to='images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    original_filename = models.CharField(max_length=255, blank=True)
    content_hash = models.CharField(max_length=64, db_index=True, null=True, blank=True)

    def __str__(self):
        return f"{self.id} - {self.image.name}"

    class Meta:
        indexes = [
            models.Index(fields=['original_filename']),
            models.Index(fields=['user', 'content_hash']),
        ]
        constraints = [
            models.UniqueConstraint(fields=['user', 'content_hash'], name='uniq_user_content_hash')
        ]