from django.conf.urls import url
from mathtutor import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'mathtutor/registration/login.html'}, name="login"),
	url(r'^logout/$', 'django.contrib.auth.views.logout',{'next_page': '/'}, name="logout"),
	url(r'^noaccess/$', views.noaccess, name='noaccess'),
	url(r'^theme-selection/$', views.theme_selection, name="theme_selection"),
	url(r'^dashboard/$', views.dashboard, name='dashboard'),
	url(r'^post-surveys/$', views.post_surveys, name="post_surveys"),
	url(r'^quiz-or-practice/(?P<category>[a-z]*)/$', views.quiz_or_practice, name="quiz_or_practice"),
    url(r'^quizes/(?P<category>[a-z]*)/$', views.list_quizes, name="list_quizes"),
	url(r'^practice/(?P<category>[a-z]*)/(?P<which>[a-z]*)/$', views.practice, name="practice"),
	url(r'^practice/(?P<category>[a-z]*)/(?P<which>[a-z]*)/(?P<itemId>\d+)/$', views.practice, name="practice_item"),
	url(r'^(?P<group>\d+)/glossary/$', views.glossary, name="glossary"),
	url(r'^glossary-item/(?P<item_id>\d+)/$', views.glossary, name="glossary_item"),
]



