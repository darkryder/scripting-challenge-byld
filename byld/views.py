
# MAY THE CODE BE WITH YOU


from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import timezone
from django.views.generic.base import View
from django.core.context_processors import csrf

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from byld.models import Team, Answer, Question, CompetetionTimeConfiguration

from django import forms
from nocaptcha_recaptcha.fields import NoReCaptchaField

import json
import urllib2, urllib
import requests
import datetime

timezone.localtime(timezone.now())

class SignUpForm(forms.ModelForm):

	username = forms.CharField(required = True, widget = forms.TextInput(attrs = {'class' : 'form-control',
																				  'placeholder' : 'Something Creative',
																				  'autocomplete' : 'off',
																				  'name' : 'user'}))

	password = forms.CharField(required = True, widget = forms.PasswordInput(attrs = {'class' : 'form-control',
																					  'placeholder' : 'Something Secure',
																					  'name' : 'pass'}))

	email = forms.EmailField(required = True, widget = forms.EmailInput(attrs = {'class' : 'form-control',
																				 'placeholder' : 'Something to communicate to',
																				 'autocomplete' : 'off',
																				 'name' : 'email'}))

	captcha = NoReCaptchaField()

	class Meta:
		model = User
		fields = ('username', 'password', 'email')

class SignInForm(forms.Form):

	username = forms.CharField(required = True, widget = forms.TextInput(attrs = {'class' : 'form-control',
																				  'placeholder' : 'Your identity',
																				  'autocomplete' : 'off',
																				  'name' : 'user'}))

	password = forms.CharField(required = True, widget = forms.PasswordInput(attrs = {'class' : 'form-control',
																					  'placeholder' : 'Your Something Secure',
																					  'name' : 'pass'}))
class HashForm(forms.Form):

	hashField = forms.CharField(required = True, widget = forms.TextInput(attrs = {'class' : 'form-control',
																				  'placeholder' : 'hash',
																				  'autocomplete' : 'off',
																				  'name' : 'hash'}))

def home(request):
	args = {}
	args.update(csrf(request))

	if request.user.is_authenticated():
		return HttpResponseRedirect("/challenges")
	else:
		args["form"] = SignInForm()

		if request.method == "POST":
			form = SignInForm(request.POST)
			args['form'] = form

			if form.is_valid():
				user = authenticate(username = request.POST["username"], password = request.POST["password"])

				if user is not None:
					if user.is_active:
						login(request, user)
					return HttpResponseRedirect("/challenges")

				else:
					form.add_error(None, "Wrong Team name / Password")


		return render_to_response("welcome.html", args)

def signout(request):
	logout(request)
	return HttpResponseRedirect("/")

def register(request):
	args = {}
	args.update(csrf(request))
	args["reg"] = False

	if request.user.is_authenticated():
		return HttpResponseRedirect("/")

	if request.method == "POST":

		form = SignUpForm(request.POST)

		captach_response = requests.post("https://www.google.com/recaptcha/api/siteverify",
										 data={'secret': "6LcbFg4TAAAAAITqrBWuwH2S9GOk_zO10quel8E1",
											   'response': request.POST["g-recaptcha-response"]})

		verdict = json.loads(captach_response.text)['success']

		state = False

		if verdict == True:

			if form.is_valid():
				state = True

			elif 'captcha' in form.errors.keys():
				form.errors.pop('captcha')
				state = True

		else:
			args['form'] = form
			return render_to_response("register.html", args)

		if state == True:

			if User.objects.filter(username = request.POST["username"]).exists():
				args['form'] = form
				return render_to_response("register.html", args)

			elif User.objects.filter(email = request.POST["email"]).exists():

				form.add_error(None, "Email ID already registered :(")
				args['form'] = form
				return render_to_response("register.html", args)

			else:
				user = User.objects.create_user(username = request.POST["username"],
												password = request.POST["password"],
												email 	 = request.POST["email"])

				newTeam = Team(team = user)
				newTeam.save()

				# newGameStatus = GameStatus(team = newTeam)
				# newGameStatus.save()

				args["reg"] = True
				return render_to_response("register.html", args)
		else:
			args['form'] = form
			return render_to_response("register.html", args)

		return HttpResponse("created")
	else:
		args['form'] = SignUpForm()
		return render_to_response("register.html", args)

def leaderboard(request):
	args = {}
	args.update(csrf(request))

	teams = Team.objects.all()

	def sorting_cmp(x, y):
		if x.score > y.score: return -1
		if x.score < y.score: return 1
		if x.last_question_solved < y.last_question_solved: return -1
		return 1

	teams = sorted(teams, cmp=sorting_cmp)
	args['teams'] = teams
	return render_to_response("leaderboard.html", args)

def updateScore(i):
	fileName = "game" + str(i) + ".txt"

	f = open(fileName, 'r')
	score = float(f.readline())
	f.close()

	f = open(fileName, 'w')
	f.write(str(score * 0.9))
	f.close()

	return score

def challenges(request):
	GAMEDATE = CompetetionTimeConfiguration.objects.get().GAMEDATE
	GAMEEND = CompetetionTimeConfiguration.objects.get().GAMEEND
	GAMELENGTH = (GAMEEND - GAMEDATE).total_seconds()

	args = {}
	args.update(csrf(request))
	args["error"] = "Please log in to continue"

	if request.user.is_authenticated():
		form = HashForm()
		team = Team.objects.get(team = request.user)

		args["gameDate"] = timezone.localtime(GAMEDATE)

		args["gameOn"] = False
		args["gameOver"]  = False

		if GAMEDATE < timezone.now() and (timezone.now() - GAMEDATE).total_seconds() <  GAMELENGTH:
			args["gameOn"] = True
		elif GAMEEND < timezone.now():
			args["gameOver"] = True

		args["timeLeft"] = (GAMEEND - timezone.now()).total_seconds()

		if request.method == "POST":
			request.POST._mutable = True	# hacks for life

			form = HashForm(request.POST)

			if form.is_valid():
				hashSubmitted = form.cleaned_data["hashField"]

				match = Answer.objects.filter(hash = hashSubmitted.strip())
				if not match:
					form.add_error("hashField", "Hash submitted is invalid")
				else:
					answer = match[0]
					question = answer.question
					if question in team.solved_questions.all():
						form.add_error("hashField", "You've already solved this question")
					else:
						question.solved_by.add(team)
						question.save()
						team.score += question.points
						team.last_question_solved = timezone.now()
						team.save()
						form.add_error("",
							"Congrats! Question solved !. %d points added" % question.points)

		args["form"] = form
		args["team"] = Team.objects.get(team = request.user)
		args['all_questions'] = Question.objects.all()
		return render(request, "challenges.html", args)
	else:
		return HttpResponseRedirect("/", args)


def secret_question(request):
	GAMEDATE = CompetetionTimeConfiguration.objects.get().GAMEDATE
	GAMEEND = CompetetionTimeConfiguration.objects.get().GAMEEND
	GAMELENGTH = (GAMEEND - GAMEDATE).total_seconds()

	if GAMEDATE < timezone.now() and (timezone.now() - GAMEDATE).total_seconds() <  GAMELENGTH:
		return render(request, "secret_question.html")
	else:
		return redirect('/')
