from django.conf.urls import patterns, include, url

from django.http import HttpResponseRedirect
from blog_app.views import *



urlpatterns = patterns('',
	url(r'^$', lenta_mask, {'mask': ""}),
	
	url(r'^about/$', about),
	url(r'^item/(?P<item_id>\d+)/$', item),	
	url(r'^restricted/', include('Svetanyashmyash.urls_restricted')),
	url(r'^search/', search),
	url(r'^register/$', register, name='register'),
	url(r'^get_more/$', get_more ),
	url(r'^redaction/$', redaction ),
)
urlpatterns += patterns(
    'django.views.static',
    (r'media/(?P<path>.*)',
    'serve',
    {'document_root': settings.MEDIA_ROOT}), )

urlpatterns += patterns('',
	url(r'^play/$', lenta_mask, {'mask': 'Спектакль'}),
	url(r'^premiere/$', lenta_mask, {'mask': 'Премьера'}),
	url(r'^news/$', lenta_mask, {'mask': 'Новость'}),
	url(r'^person/$', lenta_mask, {'mask': 'Личность'}),
	url(r'^workshop/$', lenta_mask, {'mask': 'Мастерская'}),
	url(r'^(?P<mask>author/[\w\s]+)/$', lenta_mask),
)