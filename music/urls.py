from django.conf.urls import patterns, url

from music import views

urlpatterns = patterns('',
    url(r'^<year>$', views.topSong_view, name='year'),
)