from django.core.management.base import BaseCommand, CommandError
from mathtutor.models import Quizes, QuizGroup,  LearnType, LearnItem, SubCatagory
from django.contrib.auth.models import User
import csv, os
from codecs import encode
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings


class Command(BaseCommand):

	def handle(self, *args, **options):
		BASE_DIR = getattr(settings, 'BASE_DIR', None)
		csvDir = os.path.join(BASE_DIR, 'import-items')
		with open(os.path.join(csvDir, 'learn.csv'), 'rb') as f:
			mycsv = csv.reader(f)
			next(mycsv, None) # Skip the headers
			for row in mycsv:
				SubCatagory.objects.get_or_create(name=row[5])
		f.close()
		with open(os.path.join(csvDir, 'learn.csv'), 'rb') as f:
			mycsv = csv.reader(f)
			next(mycsv, None) # Skip the headers
			for row in mycsv:
				new, created = LearnItem.objects.get_or_create(l_path=row[4], l_category=row[2].lower())
				LearnItem.objects.filter(id=new.id).update(l_title=row[3], l_image=row[6])
				l = LearnItem.objects.get(id=new.id)

				quizgroup = QuizGroup.objects.get(group=row[1])
				quizgroup.learnitem_set.add(l)

				self.stdout.write("%s" % row[0])

				learntype, created = LearnType.objects.get_or_create(name=row[0])
				learntype.learnitem_set.add(l)

				subcatagory = SubCatagory.objects.get(name=row[5])
				subcatagory.learnitem_set.add(l)


