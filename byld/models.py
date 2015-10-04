from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Team(models.Model):

	team = models.ForeignKey(User)
	score = models.IntegerField(default = 0)
	last_question_solved = models.DateTimeField(default=timezone.now)

	def __unicode__(self):
		return str(self.team.username)

class Question(models.Model):
    description = models.CharField(max_length=1024)
    points = models.IntegerField(default=0, max_length=1000)
    solved_by = models.ManyToManyField(Team, related_name='solved_questions')
    title = models.CharField(max_length=128, default="")

    def __unicode__(self):
        return "%s: [%s]" % (str(self.description),
            ' '.join([str(x) for x in self.answers.all()]))

class Answer(models.Model):
    description = models.CharField(max_length=100, blank=True, default="")
    hash = models.CharField(max_length=64)
    question = models.ForeignKey(Question, related_name='answers') # allow O2M

    def __unicode__(self):
        return "(%s)<%s>;" % (self.description, self.hash)
