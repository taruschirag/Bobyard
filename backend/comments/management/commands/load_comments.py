import json
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import connection, models
from django.utils import timezone
from django.utils.dateparse import parse_datetime

from comments.models import Comment


class Command(BaseCommand):
    help = "Load initial comments from a JSON file into the database."

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            dest='file',
            default=str(Path(settings.BASE_DIR) / 'data' / 'comments_seed.json'),
            help='Path to the seed JSON file.',
        )

    def handle(self, *args, **options):
        file_path = Path(options['file'])
        if not file_path.exists():
            self.stderr.write(self.style.ERROR(f'File not found: {file_path}'))
            return

        with file_path.open(encoding='utf-8') as handle:
            payload = json.load(handle)

        comments = payload.get('comments', [])
        loaded = 0
        for entry in comments:
            try:
                comment_id = int(entry.get('id')) if entry.get('id') is not None else None
            except (TypeError, ValueError):
                comment_id = None

            parsed_date = parse_datetime(entry.get('date')) if entry.get('date') else None
            date_value = parsed_date or timezone.now()
            defaults = {
                'author': entry.get('author'),
                'text': entry.get('text') or '',
                'date': date_value,
                'likes': entry.get('likes', 0) or 0,
                'image': entry.get('image', '') or '',
            }

            if comment_id:
                Comment.objects.update_or_create(id=comment_id, defaults=defaults)
            else:
                Comment.objects.create(**defaults)
            loaded += 1

        self._reset_sequence()
        self.stdout.write(self.style.SUCCESS(f'Loaded {loaded} comments from {file_path}'))

    def _reset_sequence(self):
        if connection.vendor != 'postgresql':
            return

        max_id = Comment.objects.aggregate(models.Max('id'))['id__max']
        if max_id is None:
            return

        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT setval(pg_get_serial_sequence(%s, %s), %s, true);",
                [Comment._meta.db_table, 'id', max_id],
            )
