from django.core.management.base import BaseCommand, CommandError
from mathtutor.models import Quiz, QuizGroup
import csv, os
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

class Command(BaseCommand):

	def handle(self, *args, **options):
		BASE_DIR = getattr(settings, 'BASE_DIR', None)
		csvDir = os.path.join(BASE_DIR, 'import-items')
		with open(os.path.join(csvDir, 'quizes.csv'), 'rb') as f:
			mycsv = csv.reader(f)
			next(mycsv, None) # Skip headers
			for row in mycsv:
				new, created = Quiz.objects.get_or_create(q_id=row[0].replace(" ",''))
				new.q_name = row[1]
				new.q_category = row[3]
                                new.site = row[4]
				new.save()
				b, created = QuizGroup.objects.get_or_create(group=row[2])
				b.quiz_set.add(new)
		f.close()
