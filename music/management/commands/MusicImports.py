from urllib import urlopen
from bs4 import BeautifulSoup, NavigableString
from django.core.management.base import BaseCommand, CommandError
from music.models import TopSong
from datetime import datetime
import re

def getStringContents(element):
	contents = ""
	for child in element.descendants:
		#import pdb; pdb.set_trace()
		if isinstance(child,NavigableString):
			contents+=child
		if child.name == 'br':
			break
	return contents

def getSong(element):
	contents = ""
	for child in element.descendants:
		#import pdb; pdb.set_trace()
		if isinstance(child,NavigableString):
			contents+=child
		if child.name == 'sup':
			break
	return contents

def getArtist(element):
	artist = element.find('sup')
	contents = ""
	for child in artist.descendants:
		if isinstance(child,NavigableString):
			contents+=child
		if element.name == 'br':
			break
	return contents

def getUrlForYear(year):
	if year>=1959:
		return "http://en.wikipedia.org/wiki/List_of_Billboard_Hot_100_number-one_singles_of_%d"%year
	else:
		return "http://en.wikipedia.org/wiki/List_of_Billboard_number-one_singles_of_%d"%year
def getSinglesForYear(year):
	text = urlopen(getUrlForYear(year)).read()
	months = 'January,February,March,April,May,June,July,August,September,October,November,December'.split(',')
	soup = BeautifulSoup(text)
	skipSongs = 0 
	skipArtist = 0
	topSongs = list()
	print year
	#import pdb; pdb.set_trace()
	for item in soup.find_all('table'):
		headers = item.find_all('th')
		headerStrings = [header.string for header in headers]
		th = item.find('th')
		if not th or not th.string:
			if not item.tr:
				continue
			if not item.tr.td:
				continue
			if not item.tr.td.b:
				continue
			th = item.tr.td.b		
		if th.string.lower() == 'issue date':
			for row in item.find_all('tr'):
				date = row.find(['th','td'])
				if date.string.lower() == 'issue date':
					continue
				if 'Artist(s)' in headerStrings:
					if skipSongs == 0:
						songTD = date.find_next_sibling('td')
						skipSongs = int(songTD.get('rowspan',1))-1
						song = getStringContents(songTD)

						if skipArtist <= 0:
							artistTD = songTD.find_next_sibling('td')
							artist = getStringContents(artistTD)
							skipArtist= int(artistTD.get('rowspan',1))
					else:
						skipSongs-=1
					skipArtist-=1
				else: #1950-1958
					if skipSongs == 0:
						songTD = date.find_next_sibling('td')
						skipSongs = int(songTD.get('rowspan',1))-1
						song = getSong(songTD)
						artist = getArtist(songTD)
					else:
						skipSongs-=1
				song = song.replace('"','')
				date = date.string
				#print ord(date[7])
				month,day = re.split('[ \t\n\xA0]+',date, maxsplit = 2)
				month = months.index(month)+1 
				day = int(day)
				topSongs.append((year,month,day,song,artist))

	return topSongs

def saveTopSong(year,month,day,song,artist):
	date = datetime(year,month,day)
	existing = list(TopSong.objects.filter(date = date))
	if existing:
		content = existing[0]
		content.song = song
		content.artist = artist
	else:
		content = TopSong(date = date, artist = artist, song = song)
	content.save()

class Command(BaseCommand):
	def  handle(self, year = None, **options):
		singles = list()
		if year ==None:
			for year in range (1940, datetime.now().year+1):
				singles += getSinglesForYear(year)
		else:
			singles += getSinglesForYear(int(year))
		for single in singles:
			saveTopSong(*single)
