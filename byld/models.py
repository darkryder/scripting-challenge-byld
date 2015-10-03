from django.db import models
from django.contrib.auth.models import User

class Team(models.Model):

	team = models.ForeignKey(User)
	score = models.FloatField(default = 0.0)

class GameStatus(models.Model):

	team = models.ForeignKey(Team)

	gameOne = models.BooleanField(default = False)
	gameTwo = models.BooleanField(default = False)
	gameThree = models.BooleanField(default = False)
