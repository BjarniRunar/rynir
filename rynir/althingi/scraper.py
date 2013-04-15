import threading
import time
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


class BootStrapper(threading.Thread):
  def run(self):
    mp = metaparser.MetaParser()
    mp.bootstrap()

    # FIXME: Manually add some metadata to the political parties.
    for fl in Flokkur.objects.all():
      stafur = settings.RYNIR_BOKSTAFIR.get(fl.abbr[:2])
      if stafur:
        fl.stafur = stafur
        fl.save()

    # FIXME: This is hard-coding the values for the 138-141st term.
    for t in (141, 140, 139, 138):
      for i in range(1, 169+1):
        mp.scrape_and_parse(('http://www.althingi.is/altext/%d/f%3.3d.sgml'
                             ) % (t, i))
        #time.sleep(2)



def bootstrap(request):
  BootStrapper().start()
  return HttpResponse('OK, started background bootstrap thread.\n'
                      'This takes about 15 minutes.')

