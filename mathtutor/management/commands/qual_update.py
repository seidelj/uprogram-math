from django.core.management.base import BaseCommand, CommandError
from mathgame.models import Student, Quizes, QuizGroup, Results, MisfitNames
from django.contrib.auth.models import User
import csv, os, requests, json
from codecs import encode
from django.core.exceptions import ObjectDoesNotExist


	
def get_group(user):
	grade = int(user.student.grade)
	if grade <= 4:
		group = 1
	elif 4 < grade <= 6:
		group = 2
	else:
		group = 3
	return group


class Command(BaseCommand):
	

	def handle(self, *args, **options):
		
		
		for q in Quizes.objects.all():

			# Call to qualtrics
			api_string = "https://survey.qualtrics.com/WRAPI/ControlPanel/api.php?API_SELECT=ControlPanel&Version=2.3&Request=getLegacyResponseData&User=econ%20ra&Token=h6ylmTK5Jr5yQhjHNwJrAmWzJCQl1UomFJAZIIS9&Format=JSON&SurveyID="
			api_call = "%s%s" % (api_string, q.q_id)
			r = requests.get(api_call)
			data = r.json()
			#self.stdout.write('%s' % data)
			
			for response_id in data:
				try:
					score = str(data[response_id]['Score']['Sum'])
				except TypeError:
					score = str(data[response_id]['Score'])
				finished = data[response_id]['Finished']
				
				if score == '': #and finished == u'1':
					score = "0"	
			
				if Results.objects.filter(response_id=response_id).count() > 0:
					# CHecks if previously not finished and updates according
					if Results.objects.get(response_id=response_id).finished == "0" and data[response_id]['Finished'] == u'1':
						Results.objects.filter(response_id=response_id).update(score=encode(score,'utf-8'), finished="1")
					else:
						continue
				
				new_r = Results(response_id=response_id,score=encode(score, 'utf_8'),finished=finished)
				#new_r.response_id = response_id
				#new_r.score = encode(score, 'utf-8')
				#new_r.finished = finished
				new_r.save()
				
				# Associate with Quizes
				quiz = Quizes.objects.get(q_id=q.q_id)
				r = Results.objects.get(id=new_r.id)
				quiz.results_set.add(r)
				
				# Associate with user
				temp_uname = encode(data[response_id]['Name'],'utf_8')
				uname = temp_uname.replace("Doe, ", "")
				#self.stdout.write('%s' % uname)
				try: 
					user = User.objects.get(username=uname)
					user.results_set.add(r)
				
				except ObjectDoesNotExist:
					new_misfit = MisfitNames(username=uname)
					new_misfit.save()
				# Only adds if quiz is in user's group.
				
						