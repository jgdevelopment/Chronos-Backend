from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import urllib2
import json
import csv

class Command(BaseCommand):

	def __init__(self, **kwargs):
		BaseCommand.__init__(self, **kwargs)

	def handle(self, **options):
		zips = self.loadZips()
		token = settings.NOAA_TOKEN
		offset = 1
		while True:
			req = urllib2.Request('http://www.ncdc.noaa.gov/cdo-web/api/v2/locations?&locationcategoryid=ZIP&sortfield=name&sortorder=desc&limit=1000&offset=%d'%offset)
			req.add_header('token', token)
			r = urllib2.urlopen(req)
			locations = json.loads(r.read())
			for location in locations['results']:
				zipCode = location['id'][4:]
				latitude,longitude = zips[zipCode]
				mindate = location['mindate']
				maxdate = location['maxdate']
				location = Location(
					stationId= zipCode,
					startDate = mindate,
					endDate = maxdate, 
					latitude = latitude,
					longitude = longitude)
				
			metadata = locations['metadata']['resultset']
			limit = metadata['limit']
			offset = metadata['offset']
			count = metadata['count']
			offset = limit+offset
			if count<offset:
				break

	def loadZips(self):
		lines = csv.DictReader(open('zipcode.csv'))
		zips = dict()
		for row in lines:
			zips[row['zip']] = (float(row['latitude']),float(row['longitude']))
		return zips
			