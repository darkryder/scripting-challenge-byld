from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$', 		  	'byld.views.home',   name = 'home'),
    url(r'^signout/$', 	'byld.views.signout', name = 'signout'),
    url(r'^register/$', 'byld.views.register', name = 'register'),

)