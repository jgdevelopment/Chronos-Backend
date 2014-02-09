from django.core.management.base import BaseCommand, CommandError
from weather.models import Location, Observation
from django.db import IntegrityError
from datetime import datetime
import csv

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
