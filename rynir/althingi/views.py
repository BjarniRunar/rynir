import hashlib
import os
import urllib2

from django.http import HttpResponse, Http404

import settings
from althingi.models import *


def AccessDenied(Exception):
  pass


def index(request):
  return HttpResponse('Welcomes to the Althings!')

def fundur(request, fundur_id=None):
  return HttpResponse('Fundur: %s' % fundur_id)

def scrape(request, proto=None, domain=None, path=None):
  if proto and domain:
    if domain not in settings.RYNIR_SCRAPE_WHITELIST:
      raise AccessDenied('Illegal scrape reqest')
    url = '%s://%s/%s' % (proto, domain, path)
    qs = request.META.get('QUERY_STRING', None)
    if qs:
      url += '?' + qs

    scrape_id, data = cached_get(url)
    if data is not None:
      return HttpResponse('OK')
    else:
      return HttpResponse('No data')

  else:
    # FIXME: Process the ScraperJob queue?
    return HttpResponse('Should process queue?')

def cached_get(url):
  cache_id = hashlib.md5(url).hexdigest()[:20]
  cache_fn = os.path.join(settings.RYNIR_SCRAPE_PATH, cache_id)
  try:
    if not os.path.exists(cache_fn):
      data = urllib2.urlopen(url).read()
      open(cache_fn, 'wb').write(data)
    return (cache_id, open(cache_fn, 'rb').read())
  except (OSError, IOError):
    return (cache_id, None)

