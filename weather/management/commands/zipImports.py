from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from weather.models import Location
import urllib2
import json
import csv
from datetime import datetime
from django.utils import datetime_safe
#patch django mktime function leap seconds
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
				if zipCode not in zips:
					continue
				latitude,longitude = zips[zipCode]
				print location
				mindate = datetime.strptime(location['mindate'],"%Y-%m-%d")
				maxdate = datetime.strptime(location['maxdate'],"%Y-%m-%d")
				location = Location(
					stationId= zipCode,
					startDate = mindate,
					endDate = maxdate, 
					latitude = latitude,
					longitude = longitude)
				print location
				#import pdb; pdb.set_trace()
				location.save()
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
			