from django.core.management.base import BaseCommand, CommandError
from mathgame.models import Student, Quizes, QuizGroup, Results, MisfitNames
from django.contrib.auth.models import User
import csv, os, json, requests, gc, sys, grequests
from codecs import encode
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from django.core.management import call_command


## HIT THE DATABASE LESS

class Command(BaseCommand):
	
	def handle(self, *args, **options):
	
		self.stdout.write("%s: Begin!" % str(datetime.now()))
		
		api_string = "https://survey.qualtrics.com/WRAPI/ControlPanel/api.php?API_SELECT=ControlPanel&Version=2.3&Request=getLegacyResponseData&User=econ%20ra&Token=h6ylmTK5Jr5yQhjHNwJrAmWzJCQl1UomFJAZIIS9&Format=JSON&SurveyID="
		
		api_urls = []
		
		for q in Quizes.objects.all():
			api_url = "%s%s" % (api_string, q.q_id)
			api_urls.append(api_url)
		
		rs = (grequests.get(u, stream=False) for u in api_urls)
		dataListDict = []
		#grequests.map(rs)
	
		qualtricsData = grequests.map(rs)
			
		#creates a dictionary of all new results
		errorInQualData = False
		
		for r in qualtricsData:
			seperator = 'SurveyID='
			try:
				before, seperator, q_id = r.url.partition(seperator)
			except AttributeError:
				errorInQualData = True
				break
			else:
				data = r.json()
				for response_id in data:
					try:
						score = str(data[response_id]['Score']['Sum'])
					except TypeError:
						score = str(data[response_id]['Score'])
					else:
						finished = data[response_id]['Finished']
						
						if score == '': #and finished == u'1':
							score = "0"	
						
						temp_uname = encode(data[response_id]['Name'])
						uname = temp_uname.replace("Doe, ", "")
						
						try:
							existingResult = Results.objects.get(response_id=response_id)
							continue
						except ObjectDoesNotExist:
							
							try:
								user = User.objects.get(username=uname)
							except ObjectDoesNotExist:
								new_misfit = MisfitNames(username=uname)
								new_misfit.save()
							else:
								quiz = Quizes.objects.get(q_id=q_id)				
								new_r = Results(name_id=user.id, response_id=response_id,score=encode(score, 'utf_8'),finished=finished, quiz_id=quiz.id )
								dataListDict.append(new_r)
								
		if errorInQualData:
			self.stdout.write("Connection to Qualtrics Timed out")
			#del qualtricsData, r, data, dataListDict, api_urls, rs, q_id, api_string, api_url
		else:
			Results.objects.bulk_create(dataListDict)
			gc.collect()
			#del qualtricsData, r, data, dataListDict, api_urls, rs, q_id, api_string, api_url
			
			
			self.stdout.write("%s: DONE" % str(datetime.now()))
	