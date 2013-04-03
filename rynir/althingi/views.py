import os

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

def thingmenn(request, thingmadur_id=None):
  thingmenn = []
  for thm in Thingmadur.objects.order_by('nafn'):
    thingmenn.append({
      'nafn':   thm.nafn,
      'stafir': thm.stafir,
      'stafur': thm.nafn[0].lower(),
      'url':    thm.url_vefs,
      'mynd':   thm.url_mynd
    })

  t = loader.get_template('althingi/thingmenn.html')
  c = Context({
    'base': settings.TEMPLATE_BASE,
    'thingmenn': thingmenn
  })
  return HttpResponse(t.render(c))

def frumvorp(request, frumvarp_id=None):
  t = loader.get_template('althingi/frumvorp.html')
  c = Context({
    'base': settings.TEMPLATE_BASE
  })
  return HttpResponse(t.render(c))

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
