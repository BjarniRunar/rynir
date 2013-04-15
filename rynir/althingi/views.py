import os

from django.http import HttpResponse, Http404
from django.template import Context, loader
from django.views.decorators.cache import cache_control

import settings
from althingi.models import *


def AccessDenied(Exception):
  pass


## Views ##

@cache_control(must_revalidate=False, max_age=3600)
def index(request):
  t = loader.get_template('althingi/index.html')
  c = Context({
    'base': settings.TEMPLATE_BASE
  })
  return HttpResponse(t.render(c))

@cache_control(must_revalidate=False, max_age=3600)
def thingmenn(request, thingmadur_id=None):
  thingmenn = []
  data = {
    'base': settings.TEMPLATE_BASE,
    'thingmenn': thingmenn
  }

  for thm in Thingmadur.objects.order_by('nafn'):
    thingmenn.append({
      'nafn':   thm.nafn,
      'stafir': thm.stafir,
      'stafur': thm.nafn[0].lower(),
      'url':    thm.url_vefs,
      'mynd':   thm.url_mynd
    })

  if thingmadur_id:
    data['thingmadur'] = {
    }

  t = loader.get_template('althingi/thingmenn.html')
  return HttpResponse(t.render(Context(data)))

@cache_control(must_revalidate=False, max_age=3600)
def kosningar(request, kosning_uid=None):
  kosningar = []
  data = {
    'base': settings.TEMPLATE_BASE,
    'kosningar': kosningar
  }
  for kosn in Kosning.objects.order_by('timi'):
    sparks = kosn.sparks()
    mixed = str(('afbrig' in kosn.titill.lower()) or
                ('J' in sparks and 'N' in sparks) or
                ('F' in sparks and 'S' in sparks)).lower()
    kosningar.append({
      'uid': 1234,
      'mixed': mixed,
      'umfang': kosn.umraeda.umfang,
      'sparks': sparks,
      'titill': kosn.titill
    })
  kosningar.sort(key=lambda k: -k['umfang'])

  t = loader.get_template('althingi/kosningar.html')
  return HttpResponse(t.render(Context(data)))

@cache_control(must_revalidate=False, max_age=86400)
def static(request, filename):
  if '..' in filename:
    raise AccessDenied
  while filename.startswith('/'):
    filename = filename[1:]

  path = os.path.join(settings.RYNIR_DIR, 'althingi', 'static', filename)
  try:
    return HttpResponse(open(path, 'rb').read(),
                        mimetype=GuessMimeType(path))
  except:
    raise Http404()


## Helpers ##

def GuessMimeType(path):
  mimetype = 'application/octet-stream'
  if path.endswith('.png'):
    mimetype = 'image/png'
  elif path.endswith('.jpg'):
    mimetype = 'image/jpeg'
  elif path.endswith('.css'):
    mimetype = 'text/css'
  elif path.endswith('.js'):
    mimetype = 'text/javascript'
  return mimetype
