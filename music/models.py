from django.db import models
from datetime import datetime
class TopSong(models.Model):
	date = models.DateField()
	artist = models.CharField(max_length = 200)
	song = models.CharField(max_length = 200)
