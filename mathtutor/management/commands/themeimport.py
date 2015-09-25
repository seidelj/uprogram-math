from django.core.management.base import BaseCommand, CommandError
from mathtutor.models import Themes, ThemeInfo
import csv, os

from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

class Command(BaseCommand):
    def handle(self, *args, **options):
        BASE_DIR = getattr(settings, 'BASE_DIR', None)
        csvDir = os.path.join(BASE_DIR, 'import-items')
        with open(os.path.join(csvDir, 'themes.csv'), 'rb') as f:
            mycsv = csv.reader(f)
            next(mycsv, None) # skip the headers
            for row in mycsv:
                themes, created = Themes.objects.get_or_create(name=row[0], abbrv=row[1], your_task=row[7])
                info = ThemeInfo(
                    name_id=themes.id,
                    number=row[2],
                    description=row[3],
                    article=row[4],
                    level_tagline=row[5],
                    image=row[8]
                )
                info.save()
        f.close()

