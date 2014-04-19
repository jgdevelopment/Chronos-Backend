# from django.http import HttpResponse, HttpResponseRedirect, Http404
# from django.shortcuts import render, get_object_or_404
# from django.template import RequestContext, loader
# from bs4 import BeautifulSoup, NavigableString
# from django.core.urlresolvers import reverse
# from datetime import datetime, timedelta
# from django.utils import timezone
# from django.views import generic
# from urllib import urlopen
# from json import dumps
# import csv
# import re
# # mlb: http://www.shrpsports.com/mlb/stand.php?link=Y&season=2014&divcnf=div&month=May&date=4
# # nba: http://www.shrpsports.com/nba/stand.php?link=Y&season=2014&divcnf=div&month=May&date=4
# # nfl(by week): http://www.shrpsports.com/nfl/stand.php?link=Y&season=2012&divcnf=div&week=Week%2017
# # nhl: http://www.shrpsports.com/nhl/stand.php?link=Y&season=2011&divcnf=div&month=Apr&date=7
# # - 
# # Toronto:
# # 	rank: 1
# # 	division: Atlantic
# # 	win-loss: 48-34
# # ....
# # Scores:
# # 	Game 1: 
# # 		Winner: Indiana, 98
# # 		Loser: Atlanta, 86
# # 	...
# #---------------------------#
# # 			  or 			#
# #---------------------------#
# # 	Results:
# # 		Division: Atlantic
# # 			1: Torotono
# # 				Record: 48-34
# # 			2: ...
# # 				Record: ...
# # 		Scores:
# # 			Game 1: 
# # 				Winner: Indiana, 98
# # 				Loser: Atlanta, 86
# # 			...
# # in objective c goal is to have a rank list for each division and a list of all games
# # without consideration of division

# def sports_view(request, league):
# 	month = int(request.GET['month'])
#   	day = int(request.GET['day'])
#   	year = int(request.GET['year']