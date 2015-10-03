from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponseRedirect, HttpResponse

from django.views.generic.base import View
from django.core.context_processors import csrf

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from byld.models import *

from django import forms
from nocaptcha_recaptcha.fields import NoReCaptchaField

from Portal.settings import GAMEDATE, GAMEEND, GAMELENGTH, gameURLS, gameNames, gameSolutions

import json
import urllib2, urllib
import requests
import datetime

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

				form.add_error(None, "Team already Exists :(")
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

				newGameStatus = GameStatus(team = newTeam)
				newGameStatus.save()

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

	args['teams'] = Team.objects.order_by('-score')
	print Team.objects
	print args['teams']
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
	args = {}
	args.update(csrf(request))
	args["error"] = "Please log in to continue"

	if request.user.is_authenticated():
		form = HashForm()
		team = Team.objects.get(team = request.user)
		gameStatus = GameStatus.objects.get(team = team)

		args["gameDate"] = GAMEDATE

		args["gameOn"] = False

		if GAMEDATE < datetime.datetime.now() and (datetime.datetime.now() - GAMEDATE).total_seconds() <  GAMELENGTH:
			args["gameOn"] = True

		args["timeLeft"] = (GAMEEND - datetime.datetime.now()).total_seconds()

		args["gameURL1"] = gameURLS[0]
		args["gameURL2"] = gameURLS[1]
		args["gameURL3"] = gameURLS[2]

		args["gameName1"] = gameNames[0]
		args["gameName2"] = gameNames[1]
		args["gameName3"] = gameNames[2]

		if request.method == "POST":
			request.POST._mutable = True	# hacks for life

			form = HashForm(request.POST)

			if form.is_valid():
				hashSubmitted = form.cleaned_data["hashField"]

				if hashSubmitted == gameSolutions[0]:

					if gameStatus.gameOne == False:
						form.add_error("hashField", "Congrats! " + gameNames[0] + " Solved")
						form.data["hashField"] = ""
						
						team.score += updateScore(1)
						team.save()

						gameStatus.gameOne = True
						gameStatus.save()

					else:
						form.add_error("hashField", gameNames[0] + " Already Solved")
					
				elif hashSubmitted == gameSolutions[1]:

					if gameStatus.gameTwo == False:
						form.add_error("hashField", "Congrats! " + gameNames[1] + " Solved")
						form.data["hashField"] = ""
						
						team.score += updateScore(2)
						team.save()

						gameStatus.gameTwo = True
						gameStatus.save()

					else:
						form.add_error("hashField", gameNames[1] + " Already Solved")

				elif hashSubmitted == gameSolutions[2]:

					if gameStatus.gameThree == False:

						form.add_error("hashField", "Congrats! " + gameNames[2] + " Solved")
						form.data["hashField"] = ""

						team.score += updateScore(3)
						team.save()

						gameStatus.gameThree = True
						gameStatus.save()

					else:
						form.add_error("hashField", gameNames[2] + " Already Solved")

				else:
					form.add_error("hashField", "Hash submitted is invalid")

		args["form"] = form
		args["team"] = Team.objects.get(team = request.user)
		return render_to_response("challenges.html", args)
	else:
		return HttpResponseRedirect("/", args)





