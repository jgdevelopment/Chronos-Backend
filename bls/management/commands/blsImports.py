from django.core.management.base import BaseCommand, CommandError
from bls.models import AveragePrice
import csv
class Command(BaseCommand):
	def  handle(self, filename, product, **options):
		lines = csv.DictReader(open(filename))
		months = 'Jan,Feb,Mar,Apr,May,Jun,Jul,Aug,Sep,Oct,Nov,Dec'.split(',')
		for row in lines:
			for month,monthName in enumerate(months):
				month+=1
				year = row['Year']
				if row[monthName]:
					existing = list(AveragePrice.objects.filter(year=year, month = month, product=product))
					if existing:
						price = existing[0]
						price.averagePrice = float(row[monthName])
					else:
						price = AveragePrice(year=year, month = month, product = product, averagePrice=float(row[monthName]))

					price.save()
