from django.conf.urls import patterns, url
from sports import views

urlpatterns = patterns('',
	 url(r'^(?P<league>\w+)/standing/$', views.sports_view, name='league'),
)