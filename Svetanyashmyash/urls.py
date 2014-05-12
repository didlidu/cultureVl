from django.conf.urls import patterns, include, url

from blog_app.views import admin, lenta, about, redaction, search, premiera, news, personality, afisha


urlpatterns = patterns('',
	url(r'^$', lenta),
	url(r'^admin/', admin),
	url(r'^lenta/', lenta),
	url(r'^about/', about),
	url(r'^redaction/', redaction),
	url(r'^search/', search),

	url(r'^premiera/', premiera),
	url(r'^news/', news),
	url(r'^personality/', personality),
	url(r'^afisha/', afisha),
)