from django.conf.urls import patterns, include, url

from blog_app.views import *


urlpatterns = patterns('',
	url(r'^$', lenta),
	url(r'^admin_post_pic/', admin_post_pic),
	url(r'^admin/', admin),
	url(r'^lenta/', lenta),
	url(r'^item/(?P<item_id>\d+)', item),
	url(r'^search/', search),
)