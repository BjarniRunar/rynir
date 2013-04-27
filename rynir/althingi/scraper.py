# -*- coding: utf-8 -*-

import datetime
import threading
import time
import traceback
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
  def __init__(self, testing=False, fundir=None):
    threading.Thread.__init__(self)
    self.testing = testing
    self.fundir = fundir and fundir.split(',')

  def run(self):
    mp = metaparser.MetaParser()
    mp.bootstrap()

    # FIXME: Manually add some metadata to the political parties.
    for fl in Flokkur.objects.all():
      stafur = settings.RYNIR_BOKSTAFIR.get(fl.abbr[:2])
      if stafur:
        fl.stafur = stafur
        fl.save()

    # Manually add missing parliamentarians
    for althingi_id, info in settings.RYNIR_THINGMENN.iteritems():
      existing = Thingmadur.objects.filter(althingi_id=althingi_id)
      if existing:
        thm = existing[0]
      else:
        thm = Thingmadur()

      thm.althingi_id = althingi_id
      thm.stafir      = info['stafir']
      thm.varamadur   = info['varamadur']
      thm.nafn        = info['nafn']
      thm.url_vefs    = info['url_vefs']
      thm.url_mynd    = info['url_mynd']
      thm.save()

      flokkur = Flokkur.objects.filter(stafur=info['flokkur'])[0]
      Flokksseta(flokkur=flokkur, thingmadur=thm,
                 upphaf=datetime.datetime.now()).save()
      print 'Manually added %s to %s' % (thm.nafn, flokkur.nafn)

    # Manually mark who is running in next elections
    for line in settings.FRAMBOD_X13_LISTI:
      try:
        xfl, kjordaemi, saeti, nafn = line[:4]
        texti = u'%s - #%s í %s' % (xfl, saeti, kjordaemi)
        thm = Thingmadur.objects.filter(nafn=nafn)[0]
        thm.iframbodifyrir = texti
        thm.save()
        print u'%s is running for %s' % (thm.nafn, texti)
      except IndexError:
        pass
      except ValueError:
        traceback.print_exc()
        print 'Bad line: %s' % line

    # FIXME: This is hard-coding the values for the 138-141st term.
    if self.testing:
      for i in range(112, 115):
        mp.scrape_and_parse(('http://www.althingi.is/altext/%d/f%3.3d.sgml'
                             ) % (141, i))
    else:
      for t in self.fundir or (138, 139, 140, 141):
        for i in range(1, 169+1):
          mp = metaparser.MetaParser()
          mp.scrape_and_parse(('http://www.althingi.is/altext/%s/f%3.3d.sgml'
                               ) % (t, i))


def bootstrap(request, testing=False, fundir=None):
  BootStrapper(testing=testing, fundir=fundir).start()
  return HttpResponse('OK, started background bootstrap thread.\n'
                      'This may take quite a while.\n')

