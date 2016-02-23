from django.conf.urls import patterns, url, include
from django.contrib import admin
admin.autodiscover()
from control.views import *

urlpatterns = patterns('',
	url(r'^index/$',  index),
)
