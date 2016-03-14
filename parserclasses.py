import json
import website.wsgi
from django.core.exceptions import ObjectDoesNotExist
import threading
from codecs import encode
from mathtutor.models import Result, User, Quiz, ParentFormResult

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



class ThreadParse(threading.Thread):
    def __init__(self, queue, data):
        threading.Thread.__init__(self)
        self.queue = queue
        self.data = data

    def get_id(self, r):
        sep = "SurveyID="
        try:
            before, sep, after = str(r.url).partition(sep)
        except AttributeError:
            return False
        else:
            q_id, sep, after = str(after).partition("&")
            return q_id

    def get_usr(self, data, rid):
        try:
            temp_uname = encode(data[rid]["Name"])
            uname = temp_uname.replace("Doe, ", "")
        except KeyError:
            usr = False
        else:
            try:
                usr = User.objects.get(username=uname)
            except ObjectDoesNotExist:
                usr = False
        finally:
            return usr

    def get_score(self, rid, data):
        try:
            score = str(data[rid]['Score']['Sum'])
        except TypeError:
            score = str(data[rid]['Score'])
        except TypeError:
            score = str(data[rid]['score'])
        finally:
            if score == "":
                score = "0"
            return score

    def build_data_dict(self, r):
        q_id = self.get_id(r)
        if not q_id:
            return []
        try:
            data = json.loads(r.text)
        except ValueError:
            print "warning error at json loads"
            return []
        newResults = []
        for item in data:
            try:
                result = Result.objects.get(response_id=item)
            except ObjectDoesNotExist:
                pass
            else:
                continue
            usr = self.get_usr(data, item)
            if not usr:
                continue
            score = self.get_score(item,data)
            finished = data[item]['Finished']
            quiz = Quiz.objects.get(q_id=q_id)
            new_r = Result(name_id=usr.id, response_id=item, score=encode(score,'utf-8'), finished=finished, quiz_id=quiz.id)
            newResults.append(new_r)
        return newResults

    def run(self):
        while True:
            response = self.queue.get()
            results = self.build_data_dict(response)
            self.data.extend(results)
            self.queue.task_done()


class ThreadParentFormParse(ThreadParse):

    def get_usr(self, data, rid):
        try:
            temp_name = encode(data[rid]["UserID"])
            uname = temp_name.replace("Doe, ", "")
        except KeyError:
            usr = False
        else:
            try:
                usr = User.objects.get(username=uname)
            except ObjectDoesNotExist:
                usr = False
        finally:
            return usr

    def build_data_dict(self, r):
        if not r:
            return []
        qualtricsId = self.get_id(r)
        try:
            data = json.loads(r.text)
        except ValueError:
            print "waring error at parsing json"
            return []
        newResults = []
        for item in data:
            try:
                result = ParentFormResult.objects.get(response_id=item)
            except ObjectDoesNotExist:
                pass
            else:
                continue
            usr = self.get_usr(data, item)
            if not usr:
                continue
            new_r = ParentFormResult(
                completeBool = int(data[item]['Finished']),
                student_id = usr.id,
                response_id = item,
                qualtrics_id = qualtricsId,
            )
            newResults.append(new_r)
        return newResults



