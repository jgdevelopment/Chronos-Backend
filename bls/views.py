from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader
from bls.models import AveragePrice
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.forms.models import model_to_dict
from json import dumps

def product_view(request,product):
	month = int(request.GET['month'])
	year = int(request.GET['year'])
	products=list(AveragePrice.objects.filter(year=year, month = month, product=product)) 
	if products:
		return HttpResponse(dumps(model_to_dict(products[0],exclude=['id'])))
	else:
		return HttpResponse(dumps(dict(error = 'no such object')))
