from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'historical.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^stocks/', include('stocks.urls')),
    url(r'^bls/', include('bls.urls')),
    url(r'^music/', include('music.urls')),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
