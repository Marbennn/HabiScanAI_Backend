from django.db import models

class ImageHistory(models.Model):
    image = models.ImageField(upload_to='images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    original_filename = models.CharField(max_length=255, blank=True)
    content_hash = models.CharField(max_length=64, unique=True, db_index=True, null=True, blank=True)

    def __str__(self):
        return f"{self.id} - {self.image.name}"