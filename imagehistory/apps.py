from django.apps import AppConfig


class ImagehistoryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'imagehistory'

    def ready(self):
        # Import signal handlers to ensure they are registered when the app is ready
        from . import signals  # noqa: F401