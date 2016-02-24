from django.conf.urls import patterns, url, include
from django.contrib import admin
admin.autodiscover()
from control.views import *

urlpatterns = patterns('',
	url(r'^login$', login),
	url(r'^logout$', logout),
	url(r'^index/$', index),
	url(r'^adduser/$', addUser),
	url(r'^deleteuser/$', deleteUser),
	url(r'^getCIUserById/$', getCIUserById),
	url(r'^router/$', router),
	url(r'^deleteroute', deleteRouter),
	url(r'^updateRouterCommit/$', updateRouterCommit),
	url(r'^getRouterOrderStatus/$', getRouterOrderStatus),
	url(r'^routerconnect/', routerConnect),
	url(r'^order/$', order),
	url(r'^addorders', addOrders),
	url(r'^sync/$', sync),
)
