from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from django.conf.urls.static import static
from django.conf import settings
from control.views import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'route.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^route/', include('control.urls')),
    url(r'^CI/', include('control.CIurls')),
)
