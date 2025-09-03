import os
from pathlib import Path
from django.core.management.base import BaseCommand
from django.conf import settings
from imagehistory.models import ImageHistory


class Command(BaseCommand):
    help = 'Reconcile ImageHistory records with files in MEDIA_ROOT. '
    'Removes DB rows with missing files and deletes unreferenced files.'

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true', help='Only print actions without executing')
        parser.add_argument('--delete-unreferenced', action='store_true', help='Delete files not referenced in DB')

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        delete_unreferenced = options['delete_unreferenced']

        media_root = Path(settings.MEDIA_ROOT)
        images_dir = media_root / 'images'
        images_dir.mkdir(parents=True, exist_ok=True)

        # 1) Remove DB rows whose file is missing
        removed_rows = 0
        for row in ImageHistory.objects.all():
            file_path = Path(row.image.path) if row.image else None
            if not file_path or not file_path.exists():
                self.stdout.write(f"Missing file for row {row.id}; deleting row")
                removed_rows += 1
                if not dry_run:
                    row.delete()

        # 2) Optionally delete files not referenced in DB
        deleted_files = 0
        if delete_unreferenced:
            referenced = set(
                Path(obj.image.path).resolve()
                for obj in ImageHistory.objects.all() if obj.image and os.path.isfile(obj.image.path)
            )
            for path in images_dir.rglob('*'):
                if path.is_file() and path.resolve() not in referenced:
                    self.stdout.write(f"Unreferenced file: {path}")
                    deleted_files += 1
                    if not dry_run:
                        try:
                            path.unlink()
                        except Exception as e:
                            self.stderr.write(f"Failed to delete {path}: {e}")

        self.stdout.write(self.style.SUCCESS(
            f"Done. Rows removed: {removed_rows}. Files deleted: {deleted_files}."
        ))


