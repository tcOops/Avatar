from django.conf.urls import patterns, url, include
from django.contrib import admin
admin.autodiscover()
from control.views import *

urlpatterns = patterns('',
	url(r'^login$', CI_login),
	url(r'^cmd/(.*)', CI_getOrder),
	url(r'^response/(.*)', CI_orderResult),
	url(r'^(.*)', CI_post),

)
