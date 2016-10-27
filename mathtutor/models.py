from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from codecs import encode
import datetime
from django.utils import timezone
# Create your models here.

class Constants:


    investment_time = datetime.timedelta(days=9, hours=6, minutes=59)

    start_date = {
        '170': timezone.make_aware(datetime.datetime(2015, 10, 15, 8, 00), timezone.get_current_timezone()),
        '153': timezone.make_aware(datetime.datetime(2015, 10, 15, 8, 00), timezone.get_current_timezone()),
        '000': timezone.make_aware(datetime.datetime(2016, 10, 24, 16, 00), timezone.get_current_timezone()),
        '152b': timezone.make_aware(datetime.datetime(2016, 10, 13, 16, 00), timezone.get_current_timezone()),
        '152cp': timezone.make_aware(datetime.datetime(2016, 10, 27, 16, 00), timezone.get_current_timezone()),
        '152cm': timezone.make_aware(datetime.datetime(2016, 10, 28, 16, 00), timezone.get_current_timezone()),
    }

    contracts = [
        {'base': 15, 'marginal': .75},
        {'base': 10, 'marginal': 1.0},
        {'base': 5, 'marginal': 1.25},
        {'base': 10, 'marginal': 1.50},
    ]

    parent_forms = [
        dict(name='address', qid="SV_57w2e5guFd4fVWd"),
        dict(name='english', qid="SV_3lBaQupuc8gJjHn"),
        dict(name="spanish", qid="SV_6Dqs31d6DOmNaol"),
    ]

    def accessBools(self, district):
        today = timezone.make_aware(datetime.datetime.now(), timezone.get_current_timezone())
        boolList = []
        for x in range(5):
            lower = self.start_date[district] + (timezone.timedelta(7) * x)
            upper = self.start_date[district] + (timezone.timedelta(7) * (x+1))
            boolList.append(dict(available=lower <= today, date=lower))
        boolList.append(dict(available=True, date=today))
        return boolList

    learnTypes = [
        dict(key='def', name='Math Glossary' ),
        dict(key='vid', name="Web Videos with the Awesome Math Guy" ),
        dict(key='tut', name="Practice Questions w/Solution"),
    ]

    categories = {
        1:{
            'oat': 'Arithmetic and Patterns',
            'nobt': 'Big Numbers',
            'nof': 'Fractions',
            'md': 'Measurement and Data',
            'geom': 'Geometry',
            'gen': 'General',
        },
        2:{
            'eat': 'Algebraic Thinking',
            'fpr': 'Proportions and Relationships',
            'mp': 'Measurement and Data',
            'ns': 'Number System',
            'geom': 'Geometry',
            'gen': 'General',
        },
        3:{
            'ee': 'Expressions and Equations',
            'pr': 'Proportions and Relationships',
            'sp': 'Probability and Statistics',
            'ns': 'Number System',
            'geom': 'Geometry',
            'gen': 'General',
        },
        25:[
            dict(key='ns', name='Number System'),
            dict(key='ee', name='Expressions and Equations'),
            dict(key='pr', name='Proportions and Relationships'),
            dict(key='geom', name='Geometry'),
            dict(key='sp', name='Probability and Statistics'),
            dict(key='gen', name="General"),
        ],
    }

    def check_access(self, group, district, category):
        x = 0
        for item in self.categories[group]:
            if item['key'] == category:
                break
            else:
                x+=1
        return self.accessBools(district)[x]['available']


class Student(models.Model):

    stuid = models.OneToOneField(User)
    group = models.IntegerField('Group', default=0)
    treatment = models.CharField('Treatment', max_length=64)
    score = models.CharField('Test Score', max_length=8)
    percentile = models.CharField("Scored Higher", max_length=8)
    assent = models.IntegerField('Student Assent', default=0)
    consent = models.IntegerField('Parent Consent', default=0)
    district = models.CharField("District", max_length=8)

    def set_null_theme(self):
        if not hasattr(self.theme, 'abbrv'):
            print "setting null theme"
            self.theme = Theme.objects.get(abbrv="NOTHEME")
            self.save(update_fields=['theme'])

    def access_date(self):
        return Constants.start_date[self.district]

    def check_access(self):
        start = self.access_date()
        end = start + Constants.investment_time
        now = timezone.localtime(timezone.now())
        endBool = now > end
        partialAccess = start <= now
        fullAccess = start <=  now and now < end
        return dict(full=fullAccess, partial=partialAccess, end=end, endBool=endBool)

    def get_remaining_time(self):
        access_date = self.access_date()
        end_date = access_date + Constants.investment_time
        remaining = end_date - timezone.make_aware(datetime.datetime.now())
        days = int(remaining.days)
        hours = float(remaining.seconds)/3600
        return dict(nights=days+1, days=days, hours=hours, end_date=end_date)

    def get_quiz_progress(self, cat=None):
        u = User.objects.get(id=self.stuid_id)
        qg = QuizGroup.objects.get(group=str(self.group))
        if cat == None:
            total = qg.quiz_set.filter(site="math").count()
            rs = u.result_set.filter(quiz__site="math")
            passed = rs.exclude(quiz__q_category="amc").filter(score__gte=5).order_by('quiz').distinct('quiz').count()
            brainBendersPassed = rs.filter(quiz__q_category="amc").filter(score__gte=3).order_by('quiz').distinct('quiz').count()
            passed += brainBendersPassed
        else:
            score = 5 if cat != "amc" else 3
            total = qg.quiz_set.filter(site="math").filter(q_category=cat).count()
            rs = u.result_set.filter(quiz__site="math").filter(quiz__q_category=cat)
            passed = rs.filter(score__gte=score).order_by('quiz').distinct('quiz').count()

        test_completion = 100 * (float(passed)/total)
        return dict(
            testCompletion=test_completion,
            numberOfQuizes=total,
            passed=passed,
        )

    def check_parent_form_completion(self):
        u = User.objects.get(id=self.stuid_id)
        rs = u.parentformresult_set.all()
        results = {}
        for f in Constants.parent_forms:
            result = rs.filter(qualtrics_id=f['qid']).filter(completeBool=1)
            if result.count() > 0:
                results[f['name']] = True
            else:
                results[f['name']] = False
        return results



    def get_wage_rate(self):
        return Constants.contracts[int(self.treatment)-1]

    def get_wage_info(self):
        quizes = QuizGroup.objects.get(group=str(self.group))
        numberOfQuizes = quizes.quiz_set.filter(site='math').count()
        rate = self.get_wage_rate()
        possibleWage = rate['base'] + float(numberOfQuizes) * rate['marginal']
        quiz_progress = self.get_quiz_progress()
        if quiz_progress['passed'] < 2:
            earnedWage = 0
        else:
            earnedWage = rate['base'] + quiz_progress['passed'] * rate['marginal']
        wageCompletion = 100 * float(earnedWage)/possibleWage
        return dict(earned=earnedWage, completion=wageCompletion, potential=possibleWage)

class Quiz(models.Model):
    q_id = models.CharField("Quiz ID", max_length=256)
    q_name = models.CharField("Quiz Name", max_length=256)
    q_group = models.ForeignKey("QuizGroup", blank=True, null=True)
    q_category = models.CharField('Category', max_length=8)
    site = models.CharField("Website", max_length=16, default='math')

    def get_display_name(self):
        if '_G2_' in self.q_name:
            name = "Beginner"
        elif '_G3_' in self.q_name:
            name = "Intermediate"
        else:
            name = False
        return name

    def get_url(self):
        return "http://ssd.az1.qualtrics.com/SE/?SID={}".format(self.q_id)

    def get_results(self, user):
        rs = user.result_set.filter(quiz__q_id=self.q_id)
        if rs.count() > 0:
            score_list = []
            for r in rs:
                score_list.append(encode(r.score, 'utf-8'))
                score_list.sort(reverse=True)
            attempted = True
            highScore = int(score_list[0])
            numberOfQuestions = 6 if self.q_category != "amc" else 4
            percentScore = 100 * (float(highScore) / numberOfQuestions)
            attempts = rs.count()
            scoreNeeded = 5 if self.q_category != "amc" else 3
            if highScore >= scoreNeeded:
                quizPassed = True
            else:
                quizPassed = False
        else:
            attempted = False
            highScore = False
            percentScore = False
            attempts = 0
            quizPassed = False

        return dict(
            attempted=attempted,
            highScore=highScore,
            percentScore=percentScore,
            attempts=attempts,
            quizPassed=quizPassed,
        )

class QuizGroup(models.Model):
    group = models.CharField('Group', max_length=8)


def get_now():
    return timezone.now()

class Result(models.Model):
    name = models.ForeignKey(User, blank=True, null=True)
    response_id = models.CharField("Response ID", max_length=256)
    score = models.CharField('Score', max_length=16)
    finished = models.CharField("Finished", max_length=8)
    quiz = models.ForeignKey(Quiz, blank=True, null=True)
    timestamp = models.DateTimeField("Time Added", default=get_now)

class LearnType(models.Model):
    name = models.CharField("Type", max_length=8)

class SubCategory(models.Model):
    name = models.CharField('SubCategory', max_length=256)

    def get_list_of_items(self, group, category, which):
        return  self.learnitem_set.filter(l_group=group).filter(l_type__name=which).filter(l_category=category)

class LearnItem(models.Model):
    l_type = models.ForeignKey(LearnType, blank=True, null=True)
    l_group = models.ForeignKey(QuizGroup, blank=True, null=True)
    l_sub = models.ForeignKey(SubCategory, blank=True, null=True)
    l_category = models.CharField('Category', max_length=8)
    l_title = models.CharField('Title', max_length=256)
    l_path = models.CharField("Path", max_length=512)
    l_image = models.CharField("Image Name", max_length=256)

    def get_file_path(self):
        if self.l_type.name == 'def' and "everydaymath.uchicago.edu" not in self.l_path:
            return "/static/mathtutor/definitions/{}.png".format(self.l_path)
        else:
            return self.l_path

def get_now():
    return timezone.now()

class ParentFormResult(models.Model):
    student = models.ForeignKey(User, blank=True, null=True)
    response_id = models.CharField('Response ID', max_length=256)
    completeBool = models.IntegerField("Is complete", default=0)
    qualtrics_id = models.CharField("Qualtrics ID", max_length=256)

class Consent(models.Model):
    child = models.CharField("Child's Name", max_length=256)
    teacher = models.CharField("Child's Teacher", max_length=256)
    guardian = models.CharField("Name of Parent/Guardian", max_length=256)
    timestamp = models.DateTimeField("Time", default=get_now)

class ConsentForm(ModelForm):
    class meta:
        model = Consent
        fields = ['c_child', 'c_teacher', 'c_guardian',]
