import datetime
import os, re, sys, csv
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from mathtutor.models import Student
from django.utils import timezone
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):

	def handle(self, *args, **options):
		BASE_DIR = getattr(settings, 'BASE_DIR', None)
		csvDir = os.path.join(BASE_DIR, 'import-items')
		with open(os.path.join(csvDir, 'student.csv'), 'rb') as f:
			mycsv = csv.reader(f)
			next(mycsv, None) # Skip the headers
			for row in mycsv:

				usr, created = User.objects.get_or_create(username=row[0])
				usr.set_password("%s" % row[1])
				usr.save()
				stu, created = Student.objects.get_or_create(stuid=usr)
				stu.district = row[6]
				stu.group = row[2]
				stu.treatment = row[3]
				stu.score = row[4]
				stu.percentile = row[5]
				stu.save()

