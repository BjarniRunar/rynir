from django.http import HttpResponse, Http404

import settings
from althingi.models import *


def AccessDenied(Exception):
  pass


## Views ##

def index(request):
  return HttpResponse('Welcomes to the Althings!')

def fundur(request, fundur_id=None):
  return HttpResponse('Fundur: %s' % fundur_id)


