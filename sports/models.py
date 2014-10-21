from django.db import models
from datetime import datetime
class Standing(models.Model):
    sport = models.CharField(max_length = 30)
    standing = models.CharField(max_length = 4000)
    date = models.DateField()
    # delete year,month,day replace with new datefield
    year = models.IntegerField()
    month = models.IntegerField()
    day = models.IntegerField()

    #object-database vs. SQL method vs service-oriented, use SQL dateObjects
    class Meta:
    	unique_together = ("year","month","day","sport")
    	index_together = [("year","month","day","sport")]
    def __unicode__(self):
    	return '%s: %s-%s-%s'%(self.sport, self.year, self.month, self.day)
    def date(self):
    	return datetime(self.year, self.month,self.day)