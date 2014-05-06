from django.conf.urls import patterns, include, url

from django.contrib import admin
from blog_app.views import index

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
	url(r'^$', index),
)