from django.conf.urls import patterns, url

from bls import views

urlpatterns = patterns('',
    url(r'^(?P<product>\w+)/price/$', views.product_view, name='product'),
)