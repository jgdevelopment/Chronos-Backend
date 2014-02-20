from django.conf.urls import patterns, url

from stocks import views

urlpatterns = patterns('',
    url(r'^(?P<symbol>\w+)/quote/$', views.quote_view, name='quote'),
)