from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader
from sports.models import Standing
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.forms.models import model_to_dict
from json import dumps
from datetime import datetime
from django.utils.functional import Promise
from django.utils.encoding import force_text
from django.core.serializers.json import DjangoJSONEncoder


def sports_view(request, league):
	year = int(request.GET['year'])
	month = int(request.GET['month'])
	day = int(request.GET['day'])
	date = datetime(year,month,day)
	standing=list(Standing.objects.filter(date__gte=date,sport=league).order_by('date')[:1])
	if standing:
		return HttpResponse(dumps(model_to_dict(standing[0],exclude=['id']), cls=DjangoJSONEncoder))
	else:
		return HttpResponse(dumps(dict(error = 'no such object')))