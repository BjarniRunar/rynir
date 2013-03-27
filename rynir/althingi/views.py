from django.http import HttpResponse, Http404
from django.template import Context, loader

import settings
from althingi.models import *


def AccessDenied(Exception):
  pass


## Views ##

def index(request):
  t = loader.get_template('althingi/index.html')
  c = Context({
    'base': settings.TEMPLATE_BASE
  })
  return HttpResponse(t.render(c))

def fundur(request, fundur_id=None):
  return HttpResponse('Fundur: %s' % fundur_id)


