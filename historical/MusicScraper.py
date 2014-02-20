from urllib import urlopen
from bs4 import BeautifulSoup, NavigableString
text = urlopen("http://en.wikipedia.org/wiki/List_of_Billboard_Hot_100_number-one_singles_of_2013").read()
soup = BeautifulSoup(text)
skipRows = 0 
def getStringContents(element):
	for child in element.descendants:
		if isinstance(child,NavigableString):
			return child
for item in soup.find_all('table'):
	th = item.find('th')
	if not th:
		continue
	if th.string == 'Issue date':
		for row in item.find_all('tr'):
			date = row.find('th')
			if date.string == 'Issue date':
				continue
			if skipRows == 0:
				song = date.find_next_sibling('td')
				skipRows = int(song['rowspan'])-1
				artist = song.next_element.string
				import pdb; pdb.set_trace()
				song = getStringContents(song)
				date = date.string
			print date,song,artist
 