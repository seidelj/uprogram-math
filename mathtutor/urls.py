from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'registration/login.html'}),
	url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
	url(r'^noaccess/$', views.noaccess, name='noaccess'),
	url(r'^theme-selection/$', views.theme_selection, name="theme_selection"),
	url(r'^dashboard/$', views.dashboard, name='dashboard'),
	url(r'^post-surveys/$', views.post_surveys, name="post_surveys"),
	url(r'^quiz-or-practice/$', views.quiz_or_practice, name='quiz_or_practice'),
	url(r'^practice/(?P<category>[a-z]*)/(?P<which>[a-z]*)/$', views.practice, name="practice"),
	url(r'^practice/(?P<category>[a-z]*)/(?P<which>[a-z]*/(?P<itemId>\d+)/$', views.practice_item, name="practice_item")m
	url(r'^(?P<group>\d+)/glossary/$', views.glossary, name="glossary"),
	url(r'^glossary-item/(?<item_id>\d+)/$', views.glossary_item, name="glossary_item"),
]



