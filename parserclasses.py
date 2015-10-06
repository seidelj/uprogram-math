import json
import website.wsgi
from django.core.exceptions import ObjectDoesNotExist

from mathtutor.models import Result, User, Quiz

class ResponseParser:

    def __init__(self):
        pass

    def get_user(self, name):
        try:
            usr = User.objects.get(username=name)
        except ObjectDoesNotExist:
            return False
        else:
            return usr

    def get_quiz(self, q_id):
        try:
            quiz = Quiz.objects.get(q_id=q_id)
        except ObjectDoesNotExists:
            return False
        else:
            return quiz

    def parse_response(self, data):
        try:
            result = Result.objects.get(response_id=data['response_id'])
        except ObjectDoesNotExist:
            pass
        else:
            return False, "Result already exists"

        quiz = Quiz.objects.get(q_id=data['quiz'])
        if not quiz:
            return False, "No quiz exists for result"

        user = self.get_user(data['name'])
        if not user:
            return False, "User not found"

        return True, Result(
            name_id=user.id,
            response_id=data['response_id'],
            score=data['score'],
            finished=data['finished'],
            quiz_id=quiz.id,
        )







