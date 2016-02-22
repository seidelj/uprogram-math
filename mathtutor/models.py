from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from codecs import encode
import datetime
from django.utils import timezone
# Create your models here.

class Constants:

    start_date = {
        '170': timezone.make_aware(datetime.datetime(2015, 10, 15, 8, 00), timezone.get_current_timezone()),
        '153': timezone.make_aware(datetime.datetime(2015, 10, 15, 8, 00), timezone.get_current_timezone()),
        '000': timezone.make_aware(datetime.datetime(2015, 1, 1, 8, 00), timezone.get_current_timezone()),
    }

    contracts = [
        {'base': 15, 'marginal': .75},
        {'base': 10, 'marginal': 1.0},
        {'base': 5, 'marginal': 1.25},
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
            dict(key='amc', name="BRAIN BENDERS"),
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
    theme = models.ForeignKey('Theme', blank=True, null=True)
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

    def get_quiz_progress(self, cat=None):
        u = User.objects.get(id=self.stuid_id)
        qg = QuizGroup.objects.get(group=str(self.group))
        if cat == None:
            total = qg.quiz_set.all().count()
            rs = u.result_set.all()
            passed = rs.exclude(quiz__q_category="amc").filter(score__gte=5).order_by('quiz').distinct('quiz').count()
            brainBendersPassed = rs.filter(quiz__q_category="amc").filter(score__gte=3).order_by('quiz').distinct('quiz').count()
            passed += brainBendersPassed
        else:
            score = 5 if cat != "amc" else 3
            total = qg.quiz_set.filter(q_category=cat).count()
            rs = u.result_set.filter(quiz__q_category=cat)
            passed = rs.filter(score__gte=score).order_by('quiz').distinct('quiz').count()

        test_completion = 100 * (float(passed)/total)
        return dict(
            testCompletion=test_completion,
            numberOfQuizes=total,
            passed=passed,
        )


    def get_wage_rate(self):
        return Constants.contracts[int(self.treatment)-1]

    def get_wage_info(self):
        quizes = QuizGroup.objects.get(group=str(self.group))
        numberOfQuizes = quizes.quizes_set.filter(site='math').count()
        rate = self.get_wage_rate()
        possibleWage = rate['base'] + float(numberOfQuizes) * rate['marginal']
        quiz_progress = self.get_quiz_progress()
        earnedWage = rate['base'] + quiz_progress['passed'] * rate['marginal']
        wageCompletion = 100 * float(earnedWage)/possibleWage
        return dict(earned=earnedWage, completion=wageCompletion)

class Quiz(models.Model):
    q_id = models.CharField("Quiz ID", max_length=256)
    q_name = models.CharField("Quiz Name", max_length=256)
    q_group = models.ForeignKey("QuizGroup", blank=True, null=True)
    q_category = models.CharField('Category', max_length=8)
    site = models.CharField("Website", max_length=16, default='tutor')

    def get_display_name(self):
        if '_G2_' in self.q_name:
            name = "Beginner"
        elif '_G3_' in self.q_name:
            name = "Intermediate"
        else:
            name = False
        return name

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


class Result(models.Model):
    name = models.ForeignKey(User, blank=True, null=True)
    response_id = models.CharField("Response ID", max_length=256)
    score = models.CharField('Score', max_length=16)
    finished = models.CharField("Finished", max_length=8)
    quiz = models.ForeignKey(Quiz, blank=True, null=True)

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

class Consent(models.Model):
    child = models.CharField("Child's Name", max_length=256)
    teacher = models.CharField("Child's Teacher", max_length=256)
    guardian = models.CharField("Name of Parent/Guardian", max_length=256)
    timestamp = models.DateTimeField("Time", default=get_now)

class ConsentForm(ModelForm):
    class meta:
        model = Consent
        fields = ['c_child', 'c_teacher', 'c_guardian',]
