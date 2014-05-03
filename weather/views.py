from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.utils import timezone
from datetime import datetime, timedelta
from django.conf import settings
from urllib import urlopen
from weather.models import Location
import urllib2
import csv
import json
from json import dumps

def weather_view(request,stationId):
  month = int(request.GET['month'])
  day = int(request.GET['day'])
  year = int(request.GET['year'])
  date = datetime (year,month,day)
  allWeatherData = {}
  dataCoefficients = {'TMAX':1/10.0,'TMIN':1/10.0,'PRCP':10000.0,'AWND':1}
  #api claims wind is in tenths of a meter/sec but this seems wrong
  location =list(Location.objects.filter(stationId__gte=stationId,startDate__lte=date,endDate__gte=date)
    .order_by('stationId')[:1])
  if location: 
    for dataType in dataCoefficients:
      template_url = ('http://www.ncdc.noaa.gov/cdo-services/services/datasets/GHCND/locations/ZIP:'+
       '%s/datatypes/%s/data.json?year=%d&month=%02d&day=%02d&token=%s')
      url = template_url%(location[0].stationId,dataType,year,month,day,settings.NOAA_TOKEN)
      req = urllib2.Request(url)
      response = urllib2.urlopen(req)
      weather = json.loads(response.read())
      for item in weather['dataCollection']['data']:
        if datetime.strptime(item['date'],"%Y-%m-%dT00:00:00.000") == date:
          value = item['value']* dataCoefficients[dataType]
          allWeatherData[dataType] = value
    return HttpResponse(dumps(allWeatherData))
  else:
    return HttpResponse(dumps(dict(error = 'no such object')))
