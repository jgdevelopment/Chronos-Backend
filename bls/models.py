from django.db import models
from datetime import datetime
class AveragePrice(models.Model):
    product = models.CharField(max_length=200)
    year = models.IntegerField()
    month = models.IntegerField()
    averagePrice = models.FloatField()
    def __unicode__(self):
    	return '%s: %s/%s = %.3f'%(self.product, self.month, self.year, self.averagePrice)
    def date(self):
    	return datetime(self.year, self.month,1)

