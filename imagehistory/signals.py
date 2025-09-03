import os
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from .models import ImageHistory


def _delete_file_if_exists(path: str) -> None:
    if path and os.path.isfile(path):
        try:
            os.remove(path)
        except Exception:
            # Swallow errors to avoid crashing request; production should log this
            pass


@receiver(post_delete, sender=ImageHistory)
def delete_image_file_on_row_delete(sender, instance: ImageHistory, **kwargs):
    # When a row is deleted, remove its file from storage
    if instance.image and hasattr(instance.image, 'path'):
        _delete_file_if_exists(instance.image.path)


@receiver(pre_save, sender=ImageHistory)
def delete_old_file_on_change(sender, instance: ImageHistory, **kwargs):
    if not instance.pk:
        return
    try:
        old_instance = ImageHistory.objects.get(pk=instance.pk)
    except ImageHistory.DoesNotExist:
        return
    old_file = getattr(old_instance, 'image', None)
    new_file = getattr(instance, 'image', None)
    if not old_file:
        return
    if old_file and new_file and old_file.name != new_file.name:
        # File replaced; delete the old one
        if hasattr(old_file, 'path'):
            _delete_file_if_exists(old_file.path)

