from django.conf.urls import patterns, url
from weather import views

urlpatterns = patterns('',
    url(r'^(?P<stationId>\w+)/$', views.weather_view, name='weather'),
)