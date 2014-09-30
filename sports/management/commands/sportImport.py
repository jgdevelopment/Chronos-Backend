from datetime import datetime, timedelta
from urllib import urlopen
from lxml import etree
import json
from sports.models import Standing
from django.core.management.base import BaseCommand, CommandError
import re
from urlparse import urljoin

monthNames = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
class SportParsingRules(object):
	def __init__(self,sport,leagues,parseDate,getPreviousDayLink):
		self.leagues = leagues
		self.name = sport
		self.parseDate = parseDate
		self.getPreviousDayLink = getPreviousDayLink

def defaultGetPreviousDayLink(year, tree):
	return tree.xpath("//a[text()='Previous Day']")[0].attrib['href']

def nflGetPreviousDayLink(year, tree):
	linkPath = tree.xpath("//a[text()='Previous Week']")
	if not linkPath:
		weekString = 'Week%2032'
		return 'stand.php?link=Y&season=%d&divcnf=div&week=%s'%(year,weekString)
	else:
		return linkPath[0].attrib['href'] 

def parseMLBDate(dateString):
	return datetime.strptime(dateString,'%b %d in %Y season')

def parseNBADate(dateString):
	monthNumber = monthNames.index(dateString[:3])+1
	year = int(dateString[9:14].strip().replace("-",""))
	day  = int(dateString[4:6].strip())
	if monthNumber < 5:
		year+=1
	return datetime(year,monthNumber,day)

def parseNFLDate(dateString):
	datePattern = re.compile(r"(\d+).*?(\d+)") #non-greedy match as little as possible
	match = datePattern.search(dateString)
	week = int(match.group(1))-1
	year = match.group(2)
	year = int(year)
	firstDay = datetime(year,9,1).weekday()
	
	NFLStartDateByWeekDay = [8,7,13,12,11,10,9]
	firstDay = NFLStartDateByWeekDay[firstDay]

	# exception cases for when the nfl season had a change in schedule
	if year == 2001:
		if week>=2:
			week+=1
	if year == 1982:
		if 3 <= week and week <= 10:
			week+=8
	if year == 1987:
		if week>=2:
			week+=1

	date = datetime (year, 9, firstDay)
	date+=timedelta(week*7)
	return date

nba = SportParsingRules('nba',['EASTERN CONFERENCE', 'WESTERN CONFERENCE'], parseNBADate, defaultGetPreviousDayLink)
mlb = SportParsingRules('mlb',['AMERICAN LEAGUE', 'NATIONAL LEAGUE'], parseMLBDate,defaultGetPreviousDayLink)
nfl = SportParsingRules('nfl',['American Football Conference', 'National Football Conference'], parseNFLDate, nflGetPreviousDayLink)

sportDict = dict(nba=nba, mlb = mlb, nfl = nfl)
def getSport(sportString):
	sport = sportDict[sportString]
	year = datetime.now().year
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


	##press previous date; if date is later than end of season, go back a year
	url = 'http://www.shrpsports.com/%s/stand.php?link=Y&season=%d&divcnf=div&month=%s&date=%d'%(sport.name,year,month,day)
	if sport.name == "nfl":
		weekString = 'Week%2032'
		url ='http://www.shrpsports.com/%s/stand.php?link=Y&season=%d&divcnf=div&week=%s'%(sport.name,year,weekString)
	while True:
		response = urlopen(url)
		previousDate = date
		url,date,standing = parseSport(response, sport, year, url)
		if not Standing.objects.filter(sport = sport.name,year = date.year,month = date.month,day = date.day).count():
			standing = json.dumps(standing)
			standing = Standing(sport = sport.name, standing = standing,year = date.year,month = date.month,day = date.day)
			standing.save()

		if date > previousDate:
			year = year-1
			month = 'Jan'
			day = 32 # an invalid date goes to the end of the season of that year
			url = 'http://www.shrpsports.com/%s/stand.php?link=Y&season=%d&divcnf=div&month=%s&date=%d'%(sport.name,year,month,day)
			if sport.name == "nfl":
				weekString = 'Week%2032'
				url ='http://www.shrpsports.com/%s/stand.php?link=Y&season=%d&divcnf=div&week=%s'%(sport.name,year,weekString)
				
def parseSport(document, sport, year, url):
	response = {}
	htmlparser = etree.HTMLParser()
	tree = etree.parse(document,htmlparser)

	previousDayRelLink = sport.getPreviousDayLink(year, tree)
	previousDayLink = urljoin(url, previousDayRelLink)

	header = tree.xpath("//div[@class='teamseasheader']")[0].text
	dateString = header[header.find("after")+6:]
	date = sport.parseDate(dateString)
	print date, previousDayLink

	standing = {}
	for league in sport.leagues:
		standing[league] = {}
		print league
		rows = tree.xpath("//table/tr[td='%s']/../tr"%league)
		print sport
		import pdb;pdb.set_trace() # not working for nfl parse, hm and aw instead of home and away, first bolded text for nfl is PF not Divison
		for element in rows:
			if element.get('class') == 'standfont2':
				if sport == 'nfl':
					currentDivision = str(element.xpath("td/node()")[0]).strip()
				else:
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