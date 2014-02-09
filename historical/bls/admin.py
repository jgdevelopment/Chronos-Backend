from django.contrib import admin
from bls.models import AveragePrice

class AveragePriceAdmin(admin.ModelAdmin):
	model = AveragePrice
	list_display = ('product', 'date', 'averagePrice')
	list_filter = ['product', 'year', 'month']
admin.site.register(AveragePrice, AveragePriceAdmin)
