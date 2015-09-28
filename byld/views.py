from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponseRedirect, HttpResponse

from django.views.generic.base import View
from django.core.context_processors import csrf

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from byld.models import *

from django import forms

import json
import urllib2, urllib
from nocaptcha_recaptcha.fields import NoReCaptchaField
import requests

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


def home(request):
	args = {}
	args.update(csrf(request))

	if request.user.is_authenticated():
		return HttpResponseRedirect("/challenges")
	else:
		args["form"] = SignInForm()

		if request.method == "POST":
			user = authenticate(username = request.POST["username"], password = request.POST["password"])

			if user is not None:
				if user.is_active:
					login(request, user)
				return HttpResponseRedirect("/challenges")

			else:
				args["error"] = "Wrong Team Name / Password"

		return render_to_response("welcome.html", args)

def signout(request):
	logout(request)
	return HttpResponse("logged out")

def register(request):
	args = {}
	args.update(csrf(request))
	args["reg"] = False

	if request.user.is_authenticated():
		return HttpResponseRedirect("/")

	if request.method == "POST":

		form = SignUpForm(request.POST)

		captach_response = requests.post("https://www.google.com/recaptcha/api/siteverify",
								 		 data={'secret': "6LckqA0TAAAAAHi5BoXhsuItBtttojWOstznsyMX",
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

				args["reg"] = True
				return render_to_response("register.html", args)
		else:
			args['form'] = form
			return render_to_response("register.html", args)

		return HttpResponse("created")
	else:
		args['form'] = SignUpForm()
		return render_to_response("register.html", args)

def challenges(request):
	args = {}
	args.update(csrf(request))
	args["error"] = "Please log in to continue"

	if request.user.is_authenticated():
		return HttpResponse("challenges")
	else:
		return HttpResponseRedirect("/", args)





