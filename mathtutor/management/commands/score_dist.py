from django.core.management.base import BaseCommand, CommandError
from mathgame.models import Student, ScoreDistribution, CompetitionType
from django.contrib.auth.models import User
import csv, os, requests, json
from codecs import encode
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings



class Command(BaseCommand):
	
	def handle(self, *args, **options):
		BASE_DIR = getattr(settings, 'BASE_DIR', None)
		with open(os.path.join(BASE_DIR, 'scoredist.csv'), 'rb') as f:
			mycsv = csv.reader(f)
			next(mycsv, None) # Skip the headers
			for row in mycsv:
				CompetitionType.objects.get_or_create(competition=row[0])
		f.close()
		
		with open(os.path.join(BASE_DIR, 'scoredist.csv'), 'rb') as f:
			mycsv = csv.reader(f)
			next(mycsv, None) # Skip the headers
			for row in mycsv:
				new = ScoreDistribution(score=row[1], frequency=row[2])
				new.save()
				s = ScoreDistribution.objects.get(id=new.id)
				
				competitiontype = CompetitionType.objects.get(competition=row[0])
				competitiontype.scoredistribution_set.add(s)