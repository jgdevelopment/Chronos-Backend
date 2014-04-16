from django.db import models
from datetime import datetime
class Location(models.Model):
	stationId = models.CharField(max_length=200)
	startDate = models.DateTimeField()
	endDate = models.DateTimeField()
	latitude = models.FloatField()
	longitude = models.FloatField()
	def __unicode__(self):
		return '%s: %.4f, %.4f'%(self.stationId, self.latitude, self.longitude) #changed from self.name to self.stationId
	def date(self):
		return datetime(self.year, self.month,1)

class Observation(models.Model):
	location = models.ForeignKey(Location)
	temperatureMax = models.FloatField()
	temperatureMin = models.FloatField()
	precipitation = models.IntegerField()
	windSpeed = models.IntegerField()

	def __unicode__(self):
		return '%s: temperature(max/min):%.1f, %.1f precipitation:%d windSpeed:%d'%(self.location, self.temperatureMax,
		self.temperatureMin, self.precipitation, self.windSpeed)
	def date(self):
		return datetime(self.year, self.month,1)

