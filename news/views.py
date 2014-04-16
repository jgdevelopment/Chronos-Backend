from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.utils import timezone
from datetime import datetime, timedelta
from urllib import urlopen
import urllib2
import csv
import json
from json import dumps

def news_view(request):
  month = int(request.GET['month'])
  day = int(request.GET['day'])
  year = int(request.GET['year'])
  start_date = datetime (year,month,day)
 
  template_url = 'http://content.guardianapis.com/search?from-date=%02d-%02d-%02d&order-by=oldest&api-key=5gqa3c6ecrt4d3vfdr3mm65j'
  url = template_url%(year,month,day)
  req = urllib2.Request(url)
  response = urllib2.urlopen(req)
  headlines = json.loads(response.read())
  news = list()
  for article in headlines['response']['results']:
    news.append(article)
  return HttpResponse(dumps(news))