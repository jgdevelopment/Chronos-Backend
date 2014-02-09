from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.utils import timezone
from datetime import datetime, timedelta
from urllib import urlopen
import csv
from json import dumps

def quote_view(request, symbol):
  month = int(request.GET['month'])
  day = int(request.GET['day'])
  year = int(request.GET['year'])
  start_date = datetime (year,month,day)
  end_date = start_date+timedelta(days=7)
  template_url = 'http://ichart.finance.yahoo.com/table.csv?s=%s&a=%02d&b=%02d&c=%d&d=%02d&e=%02d&f=%d&g=w&ignore=.csv'
  url = template_url%(symbol,month-1,day, year, end_date.month-1, end_date.day, end_date.year)
  response = urlopen(url)
  quote = list(csv.DictReader(response))
  #assuming ordered by most recent
  quote= quote[0]
  for key,value in quote.items():
    try:
      quote[key] = float(value)
    except:
      pass
  return HttpResponse(dumps(quote))