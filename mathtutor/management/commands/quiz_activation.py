from django.core.management.base import BaseCommand, CommandError
from mathtutor.models import Quiz
import os
import requests

class Command(BaseCommand):
    help = "activates or deactivates quizes"

    def add_arguments(self, parser):
        parser.add_argument("action", nargs="+", type=str)

    def handle(self, *args, **options):
        _API_URL = os.getenv("API_URL")
        _USER_ID = os.getenv("USER_ID")
        _TOKEN = os.getenv("TOKEN")
        if options['action'][0] == "deact":
            action = "deactivateSurvey"
        elif options['action'][0] == "activ":
            action = "activateSurvey"
        else:
            raise CommandError("Invalid argument passed")

        apiCall = _API_URL + "Request=" + action + "&User=" + _USER_ID + "&Token=" + _TOKEN + "&Format=JSON" + "&Version=2.5" + "&SurveyID="
        for quiz in Quiz.objects.all():
            r = requests.get(apiCall + quiz.q_id)
            print apiCall + quiz.q_id
            print r.text


