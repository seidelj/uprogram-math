from django.core.management.base import BaseCommand, CommandError
from mathgame.models import Student, PrizeTable, ScoreDistribution, CompetitionType
from django.contrib.auth.models import User
import csv, os, requests, json
from codecs import encode
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings


class Command(BaseCommand):
	
	def handle(self, *args, **options):
		BASE_DIR = getattr(settings, 'BASE_DIR', None)
		with open(os.path.join(BASE_DIR, 'prizetable.csv'), 'rb') as f:
			mycsv = csv.reader(f)
			next(mycsv, None) # Skip the headers
			for row in mycsv:
				CompetitionType.objects.get_or_create(competition=row[0])
		f.close()
		
		with open(os.path.join(BASE_DIR, 'prizetable.csv'), 'rb') as f:
			mycsv = csv.reader(f)
			next(mycsv, None) # Skip the headers
			for row in mycsv:
				new = PrizeTable(value=row[1], frequency=row[2], percent=row[3])
				new.save()
				p = PrizeTable.objects.get(id=new.id)
				
				competitiontype = CompetitionType.objects.get(competition=row[0])
				competitiontype.prizetable_set.add(p)