from django.core.management.base import BaseCommand, CommandError
from mathgame.models import Student, PrizeTable, ScoreDistribution, CompetitionType, Quizes, Results
from django.contrib.auth.models import User
import csv, os, requests, json
from codecs import encode
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

class Command(BaseCommand):
	
	def handle(self, *args, **options):
		
		QUIZ_ID_JOE = 'SV_3eKvIBaz7W71mmx'
		BASE_DIR = getattr(settings, 'BASE_DIR', None)
		
		quiz = Quizes.objects.get(q_id=QUIZ_ID_JOE)
		
		with open(os.path.join(BASE_DIR, 'strays.csv'), 'rb') as f:
			mycsv = csv.reader(f)
			next(mycsv, None) # SKip the headers
			for row in mycsv:
				
				#name_id
				try:
					user = User.objects.get(username=row[2])
				except ObjectDoesNotExist:
					continue
				else:
					name_id = user.id
				
				#quiz_id
				quiz_id = quiz.id
				
				#score
				score = row[10]
				
				#finished
				finished = row[9]
				#response_id
				
				result, created = Results.objects.get_or_create(response_id=row[0])
				
				Results.objects.filter(id=result.id).update(name=name_id, quiz=quiz_id, score=score, finished=finished)
				

