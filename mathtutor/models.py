from django.db import models
from django.contrib.auth.models import User
from codecs import encode
import datetime

# Create your models here.

class Constants:

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
		25:{
			'ee':  'Expressions and Equations',
			'gen': 'General',
			'geom':'Geometry',
			'ns':  'Number System',
			'pr':  'Proportions and Relationships',
			'sp':  'Probability and Statistics',
		},
	}

	
class Student(models.Model):
	
	stuid = models.OneToOneField(User)
	group = models.IntegerField('Group', default=0)
	treatment = models.CharField('Treatment', max_length=64)
	score = models.CharField('Test Score', max_length=8)
	percentile = models.CharField("Scored Higher", max_length=8)
	theme = models.IntegerField('Theme', default=0)
	assent = models.IntegerField('Student Assent', default=0)
	consent = models.IntegerField('Parent Consent', default=0)
	district = models.CharField("District", max_length=8)
	
	def access_date(self):
		pass

	def get_overall_progress(self, cat=None):
		u = User.objects.get(id=self.stuid_id)
		qg = QuizGroup.objects.get(group=str(self.group))
		if cat == None:
			total = qg.quizes_set.all().count()
			rs = u.results_set.all()
			passed = rs.filter(score__gte=5).order_by('quiz').distinct('quiz').count()
		else:
			total = qg.quizes_set.filter(q_catagory=cat).count()
			rs = u.results_set.filter(q_catagory=cat).count()
			passed = rs.filter(score__gte=5).order_by('quiz').distinct('quiz').count()

		test_completion = 100 * (float(passed/total))
		return test_completion, total, passed

class Quizes(models.Model):
	q_id = models.CharField("Quiz ID", max_length=256)
	q_name = models.CharField("Quiz Name", max_length=256)
	q_group = models.ForeignKey("QuizGroup", blank=True, null=True)
	q_catagory = models.CharField('Category', max_length=8)
	
	def get_results(self, user):
		rs = u.results_set.filter(quiz__q_id=self.q_id)
		if rs.count() > 0:
		
			for r in rs:
				score_list.append(encode(r.score, 'utf-8'))
			score_list.sort(reverse=True)
			attempted = True
			highScore = int(score_list[0])
			percentScore = 100 * (float(score) / 6)
			attempts = rs.count()
			if score >= 5:
				quizPassed = True
			else:
				quizPassed = False

		else
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
		)

class QuizGroup(models.Model):
	group = models.CharField('Group', max_length=8)


class Results(models.Model):
	name = models.ForeignKey(User, blank=True, null=True)
	response_id = models.CharField("Response ID", max_length=256)
	score = models.CharField('Score', max_length=16)
	finished = models.CharField("Finished", max_length=8)
	quiz = models.ForeignKey(Quizes, blank=True, null=True)

class LearnType(models.Model):
	name = models.CharField("Type", max_length=8)

class LearnItem(models.Model):
	l_type = models.ForeignKey(LearnType, blank=True, null=True)
	l_group = models.ForeignKey(QuizGroup, blank=True, null=True)
	l_sub = models.ForeignKey(SubCatagory, blank=True, null=True)
	l_category = models.ForeignKey('Category', max_length=8)
	l_title = models.CharField('Title', max_length=256)
	l_path = models.CharField("Path", max_length=512)
	l_image = models.CharField("Image Name", max_length=256)

def get_now()
	return timezone.now()

class Consent(models.Model):
	c_child = models.CharField("Child's Name", max_length=256)
	c_teacher = models.CharField("Child's Teacher", max_length=256)
	c_guardian = models.CharField("Name of Parent/Guardian", max_length=256)
	c_timestamp = models.DateTimeField("Time", default=get_now)

class Themes(models.Model):
	name = models.CharField("Name", max_length=256)
	abbrv = models.CharField("Name Abbrevation", max_length=256)
	theme_tagline = models.CharField("Theme Tagline", max_length=512)
	your_task = models.CharField("Your Task", max_length=512)

class ThemeInfo(models.Model):
	name = models.ForeignKey(Themes)
	number =models.IntegerField("Level")
	description = models.CharField("Level Description", max_length=256)
	image = models.CharField("Image File", max_length=256)
	level_tagline = model.CharField("Level Tagline", max_length=512)
	article = models.CharField("Article", max_length=128)

class ConsentForm(ModelForm):
	class meta:
		model = Consent
		fields = ['c_child', 'c_teacher', 'c_guardian',] 
	
		
