from django.conf.urls import patterns, url, include

from blog_app.views import *
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
	url(r'^$',					restricted, name='restricted'),
	url(r'^admin_post_pic/$', 	admin_post_pic),
	url(r'^admin_get_pic/$', 	admin_get_pic),
	url(r'^admin_del_pic/$', 	admin_del_pic),	
	url(r'^edit/(?P<id>\d+)/$', edit),
	url(r'^edit/$', 			new),
	url(r'^preview/$', 			preview),
	url(r'^archive/$', 			archive),
	url(r'^profile/$', 			profile),
	url(r'^logout/$', 			user_logout),
	url(r'^login/$', 			'django.contrib.auth.views.login', {'template_name': 'blog_app/login.html'}),
	url(r'^admin/', include(admin.site.urls)),
)