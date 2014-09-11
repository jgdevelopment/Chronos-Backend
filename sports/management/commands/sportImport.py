from datetime import datetime, timedelta
from urllib import urlopen
from lxml import etree
import json
from sports.models import Standing
from django.core.management.base import BaseCommand, CommandError

monthNames = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
class SportParsingRules(object):
	def __init__(self,sport,leagues,parseDate):
		self.leagues = leagues
		self.name = sport
		self.parseDate = parseDate

def parseMLBDate(dateString):
	return datetime.strptime(dateString,'%b %d in %Y season')

def parseNBADate(dateString):
	monthNumber = monthNames.index(dateString[:3])+1
	year = int(dateString[9:14].strip().replace("-",""))
	day  = int(dateString[4:6].strip())
	if monthNumber < 5:
		year+=1
	return datetime(year,monthNumber,day)

nba = SportParsingRules('nba',['EASTERN CONFERENCE', 'WESTERN CONFERENCE'], parseNBADate)
mlb = SportParsingRules('mlb',['AMERICAN LEAGUE', 'NATIONAL LEAGUE'], parseMLBDate)

def getSport(sportString):
	if sportString == "mlb":
		mlb = SportParsingRules('mlb',['AMERICAN LEAGUE', 'NATIONAL LEAGUE'], parseMLBDate)
		sport = mlb
	if sportString == "nba":
		sport = nba
	year = 1980 #datetime.now().year
	day = 1
	month = 1

	# format JSON so it is ordered by highest record
	date = datetime(year,month,day)
	collected = Standing.objects.filter(sport = sport.leagues).order_by('year','month','day')
	items = list(collected[:1])

	if items:
		year = items[0].year
		month = items[0].month
		day = items[0].day
		date = datetime(year,month,day)
		date -= timedelta(1)
		year = date.year
		month = date.month
		month = monthNames[month-1]
		day = date.day
	else:
		date = datetime(year+1,1,31)
	# date = datetime(2013,'Jan', 32) #adds extra data from 2013 when prior block is commented out

	##press previous date; if date is later than end of season, go back a year
	url = 'http://www.shrpsports.com/%s/stand.php?link=Y&season=%d&divcnf=div&month=%s&date=%d'%(sport.name,year,month,day)
	while True:
		response = urlopen(url)
		previousDate = date
		url,date,standing = parseSport(response, sport)
		if not Standing.objects.filter(sport = sport.name,year = date.year,month = date.month,day = date.day).count():
			standing = json.dumps(standing)
			standing = Standing(sport = sport.name, standing = standing,year = date.year,month = date.month,day = date.day)
			standing.save()
		print date
		if date > previousDate:
			year = year-1
			month = 'Jan'
			day = 32
			url = 'http://www.shrpsports.com/%s/stand.php?link=Y&season=%d&divcnf=div&month=%s&date=%d'%(sport.name,year,month,day)
				
def parseSport(document, sport):
	response = {}
	htmlparser = etree.HTMLParser()
	tree = etree.parse(document,htmlparser)
	previousDayLink = tree.xpath("//a[text()='Previous Day']")[0].attrib['href']
	previousDayLink = 'http://www.shrpsports.com/%s/%s'%(sport.name,previousDayLink)
	header = tree.xpath("//div[@class='teamseasheader']")[0].text
	dateString = header[header.find("after")+6:]
	date = sport.parseDate(dateString)
	standing = {}
	for league in sport.leagues:
		standing[league] = {}
		rows = tree.xpath("//table/tr[td='%s']/../tr"%league)
		for element in rows:
			if element.get('class') == 'standfont2':
				currentDivision = str(element.xpath("td/b/node()")[0]).strip()
				standing[league][currentDivision] = {}

			if element.get('class') == 'standfont1':
				name = str(element.xpath("td/a/text()")[0])
				stats = element.xpath("td[not(a)]/node()")
				record = stats[0].strip()
				home = stats[3].strip()
				away = stats[4].strip()
				standing[league][currentDivision][name] = dict(record=record,home=home,away=away)
				
	return previousDayLink, date, standing

class Command(BaseCommand):
	def  handle(self,sportString, **options):
		getSport(sportString)