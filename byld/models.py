from random import choice
from string import ascii_letters

from django.db import models
from solo.models import SingletonModel

from django.contrib.auth.models import User
from django.utils import timezone

def make_auth():
	things = range(10)
	things.extend(ascii_letters)

	auth = []
	for _ in xrange(16):
		auth.append(str(choice(things)))
	return ''.join(auth)

class Team(models.Model):

	team = models.ForeignKey(User)
	score = models.IntegerField(default = 0)
	last_question_solved = models.DateTimeField(default=timezone.now)
	token = models.CharField(max_length=32, default=make_auth)
	ATM_ongoing = models.BooleanField(default=False)
	ATM_balance = models.IntegerField(default=10**8)

	def __unicode__(self):
		return str(self.team.username)

class Question(models.Model):
	description = models.CharField(max_length=1024)
	points = models.IntegerField(default=0, max_length=1000)
	solved_by = models.ManyToManyField(Team, related_name='solved_questions', null=True, blank=True)
	title = models.CharField(max_length=128, default="")
	hidden = models.BooleanField(default=False)

	def __unicode__(self):
		return "%s: [%s]" % (str(self.description),
			' '.join([str(x) for x in self.answers.all()]))

class Answer(models.Model):
	description = models.CharField(max_length=100, blank=True, default="")
	hash = models.CharField(max_length=64)
	question = models.ForeignKey(Question, related_name='answers') # allow O2M

	def __unicode__(self):
		return "(%s)<%s>;" % (self.description, self.hash)

class CompetetionTimeConfiguration(SingletonModel):
	GAMEDATE = models.DateTimeField(null = True, blank = True, default = timezone.now)
	GAMEEND = models.DateTimeField(null = True, blank = True, default = timezone.now)

	def __unicode__(self):
		return "Competetion Time"





