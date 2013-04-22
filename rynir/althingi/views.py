import locale
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

#@cache_control(must_revalidate=False, max_age=3600)
def thingmenn(request, thingmadur_id=None):
  flokkar = []
  thingmenn = []
  data = {
    'base': settings.TEMPLATE_BASE,
    'flokkar': flokkar,
    'thingmenn': thingmenn
  }

  fl_thm = {}
  for fl in Flokkur.objects.order_by('nafn'):
    fl_thm[fl.stafur] = []
    flokkar.append({
      'nafn': fl.nafn,
      'stafur': fl.stafur,
      'lysing': fl.lysing,
      'url': fl.url_vefs,
      'mynd': fl.url_mynd,
      'thingmenn': fl_thm[fl.stafur]
    })

  for thm in Thingmadur.objects.order_by('nafn'):
    info = {
      'nafn':   thm.nafn,
      'stafir': thm.stafir,
      'stafur': thm.nafn[0].lower(),
      'flokkur': thm.flokkur(),
      'flokksstafur': thm.flokkur().stafur,
      'maeting': thm.maeting(),
      'hlydni': thm.hlydni(),
      'url':    thm.url_vefs,
      'mynd':   thm.url_mynd
    }
    fl_thm[thm.flokkur().stafur].append(info)
    thingmenn.append(info)

  thingmenn.sort(key=lambda t: t['nafn'], cmp=locale.strcoll)

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
    try:
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
    except Umraeda.DoesNotExist:
      pass
  kosningar.sort(key=lambda k: -k['umfang'])
  data['topp50'] = kosningar[:50]
  data['topp100'] = kosningar[:100]

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
