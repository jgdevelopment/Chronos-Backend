from django.core.management.base import BaseCommand, CommandError
from weather.models import Location, Observation
from django.db import IntegrityError
from datetime import datetime
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.utils import timezone
from datetime import datetime, timedelta
from urllib import urlopen
from json import dumps
import csv


# 1: push top song to heroku (add in url)
# input zip code, day, month, year
# take inputed zip code
# output lat and long via zip code csv
# search station code csv for closest lat and long
# output closest weather station lat and long
# use closest weather station lat and long and convert to ZIP code using zipcode csv (unless ncdc allows search by ID)
# --> too slow? use url 4 times (for each data type) http://www.ncdc.noaa.gov/cdo-services/services/datasets/GHCND/locations/ZIP:'input zip code'/datatypes/'TMAX'/data.json?year='year'&month='month'&day='day'&token=lYpGKtvmKcABFWooIogXphDAkxDnDVBy
# return JSON data for specific date and dataype
# convert data value units and return values paired to their datatypes
# to do: sports: scores, game details, standings, headlines(scrape sports-reference, maybe use specific for baseball, maybe scrap shrpsports) and news (guardian headlines)
# objective-c to do: fix scroll-view bug (arrangement), add sports template, add iTunes music preview

class Command(BaseCommand):
	def __init__(self, **kwargs):
		BaseCommand.__init__(self, **kwargs)
		self.locations = dict()

	def handle(self, filename, **options):
		lines = csv.DictReader(open(filename))
		for row in lines:
			if invalidRow(row):
				continue
			self.addObservation(row)

	def getStationLocation(self,row):
		stationId = row['STATION']
		if stationId in self.locations:
			return self.locations[stationId]
		else:
			existing = list(Location.objects.filter(stationId=stationId))
			if existing:
				self.locations[stationId] = existing[0]
			else:
				self.locations[stationId] = Location(
					stationId = stationId,
					startDate= getDate(row),
					endDate=getDate(row),
					longitude=float(row['LONGITUDE']),
					latitude=float(row['LATITUDE']))
			self.locations[stationId].save()
	def addObservation(self,row):
		print self.getStationLocation(row) # = None and program fails when it is removed
		location = self.getStationLocation(row) 
		date = getDate(row)
		location.startDate = location.startDate.replace(tzinfo=None)
		location.endDate = location.endDate.replace(tzinfo=None)

		if date>=location.startDate and date<location.endDate:
			return True
		else:
			observation = Observation(
					location = location, #removed location.id because it = 1 and had to be a location.id value #foreign key check is failing raises integrity error
					temperatureMax=float(row['TMAX'])/10.0,
					temperatureMin=float(row['TMIN'])/10.0,
					precipitation=float(row['PRCP'])*10000.0,
					windSpeed=float(row['AWND'])*10.0)
			observation.save()

def getDate(row):
	date = datetime.strptime(row['DATE'],'%Y%m%d')
	return date

def invalidRow(row):
	for column in ['PRCP','TMAX','TMIN','AWND']:
		if row[column] == '9999' or row[column] == '-9999':
			return True
#build step-by-step when Tmax for station, when Tmin set Tmin, use postgres over mysql