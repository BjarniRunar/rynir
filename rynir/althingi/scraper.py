from django.http import HttpResponse, Http404

import settings
from althingi.models import *
from althingi.parsers import *


def AccessDenied(Exception):
  pass


def scrape(request, proto=None, domain=None, path=None):
  mp = metaparser.MetaParser()
  if proto and domain:
    if domain not in settings.RYNIR_SCRAPE_WHITELIST:
      raise AccessDenied('Illegal scrape reqest')
    url = '%s://%s/%s' % (proto, domain, path)
    qs = request.META.get('QUERY_STRING', None)
    if qs:
      url += '?' + qs

    if mp.scrape_and_parse(url):
      return HttpResponse('OK')
    else:
      return HttpResponse('No data')

  else:
    # FIXME: Process the ScraperJob queue?
    return HttpResponse('Should process queue?')

def bootstrap(request):
  metaparser.MetaParser().bootstrap()
  return HttpResponse('OK')
  
