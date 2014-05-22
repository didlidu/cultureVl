from django.conf.urls import patterns, include, url

from blog_app.views import *
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
	url(r'^$', lenta),
	url(r'^admin/', include(admin.site.urls)),
	url(r'^restricted/admin_post_pic/', admin_post_pic),
	url(r'^restricted/admin_get_pic/', admin_get_pic),
	url(r'^restricted/admin_del_pic/(?P<way>\w+[|]\w+[.]\w+)', admin_del_pic),	
	url(r'^restricted/edit/(?P<id>\d+)', edit),
	url(r'^restricted/edit/', new),
	url(r'^restricted/preview/', preview),
	url(r'^restricted/archive/', archive),
	url(r'^restricted/profile/', profile),
	url(r'^lenta/', lenta),
	url(r'^item/(?P<item_id>\d+)', item),
	url(r'^search/', search),
	url(r'^register/$', register, name='register'),
	url(r'^restricted/login/$', 'django.contrib.auth.views.login',  
		{'template_name': 'blog_app/login.html'}),
	url(r'^staff/$', culture ),
	url(r'^get_more/$', get_more ),

	url(r'^restricted/', restricted, name='restricted'),
	url(r'^logout/$', user_logout, name='logout'),

)
urlpatterns += patterns(
    'django.views.static',
    (r'media/(?P<path>.*)',
    'serve',
    {'document_root': settings.MEDIA_ROOT}), )