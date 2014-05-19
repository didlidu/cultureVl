from django.conf.urls import patterns, include, url

from blog_app.views import *


urlpatterns = patterns('',
	url(r'^$', lenta),
	url(r'^admin_post_pic/', admin_post_pic),
	url(r'^admin_get_pic/', admin_get_pic),
	url(r'^admin/', admin),
	url(r'^edit/(?P<id>\d+)', edit),
	url(r'^lenta/', lenta),
	url(r'^item/(?P<item_id>\d+)', item),
	url(r'^search/', search),
	url(r'^register/$', register, name='register'),
	url(r'^restricted/login/$', 'django.contrib.auth.views.login',  
		{'template_name': 'blog_app/login.html'}),
	url(r'^staff/$', culture ),
	url(r'^get_more/$', get_more ),
	url(r'^test/$', test ),

	url(r'^restricted/', restricted, name='restricted'),
	url(r'^logout/$', user_logout, name='logout'),

)
urlpatterns += patterns(
    'django.views.static',
    (r'media/(?P<path>.*)',
    'serve',
    {'document_root': settings.MEDIA_ROOT}), )