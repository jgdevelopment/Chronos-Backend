from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader
from music.models import TopSong
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.forms.models import model_to_dict
from json import dumps
from datetime import datetime
from django.utils.functional import Promise
from django.utils.encoding import force_text
from django.core.serializers.json import DjangoJSONEncoder

class DjangoJSONEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Promise):
            return force_text(obj)
        return super(DjangoJSONEncoder, self).default(obj)

def song_view(request):
	year = int(request.GET['year'])
	month = int(request.GET['month'])
	day = int(request.GET['day'])
	date = datetime(year,month,day)
	topSong=list(TopSong.objects.filter(date__gte=date).order_by('date'))
	if topSong:
		return HttpResponse(dumps(model_to_dict(topSong[0],exclude=['id']), cls=DjangoJSONEncoder))
	else:
		return HttpResponse(dumps(dict(error = 'no such object')))
