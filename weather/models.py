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
