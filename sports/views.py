from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader
from sports.models import Standing
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.forms.models import model_to_dict
from json import dumps
from bs4 import BeautifulSoup, NavigableString
from django.core.urlresolvers import reverse
from datetime import datetime, timedelta
from django.utils import timezone
from django.views import generic
from urllib import urlopen
from lxml import etree


monthNames = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
mlbDivisons = ['Eastern Division', 'Central Division','Western Division']
# sportLeagues = {'mlb':getMLB, 'nba':getNBA, 'nfl':getNFL, 'nhl':getNHL, 
# 'ncaabasketball':getNCAABasketball,'ncaafootball':getNCAAFootball}

def sports_view(request, league):
	month = int(request.GET['month'])
	day = int(request.GET['day'])
	year = int(request.GET['year'])
	standing=list(Standing.objects.filter(year=year, month = month, day=day, sport=league))
	if standing:
		return HttpResponse(dumps(model_to_dict(standing[0],exclude=['id'])))
	else:
		return HttpResponse(dumps(dict(error = 'no such object')))
# def getMLB(day,month,year):
# 	# monthName = monthNames[month-1]
# 	# baseUrl = 'www.shrpsports.com/mlb/stand.php?link=Y&season=%d&divcnf=div&month=%s&date=%d'%(year,monthName,day)
# 	# response = urlopen(baseUrl)
# 	# htmlparser = etree.HTMLParseer()
# 	# tree = etree.parse(response,htmlparser)
# 	# rows = tree.xpath("//table/tr[td='AMERICAN LEAGUE']/../tr")	
# 	# for element in rows:
# 	# 	if element['class'] == 'standfont2':
# 	# 		currentDivision = element.xpath("/td/b/node()")

# def getNBA():
# 	pass
# def getNFL():
# 	pass
# def getNHL():
# 	pass
# def getNCAABasketball():
# 	pass
# def getNCAAFootball():
# 	pass