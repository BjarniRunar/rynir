import re
import traceback

from althingi.models import *
from htmlparser import ScraperParserHTML
from metaparser import RegisterScraperParser, RegisterBootstrap


FLOKKAR_URL = 'http://www.althingi.is/vefur/thingfl.html'
FLOKKAR_RXP = FLOKKAR_URL.replace('.', '\\.').replace('?', '\\?')+'$'

SKAMMSTOFUN_RE = re.compile('\\(([^)]+)\\)')


class ScraperParserFlokkar(ScraperParserHTML):
  MATCH_URLS = (FLOKKAR_RXP, )
  SCRAPE_URLS = ( )

  def skilgreina_flokk(self, stafir, nafn, url):
    existing = Flokkur.objects.filter(stafir=stafir)
    if existing:
      fl = existing[0]
    else:
      fl = Flokkur()
                
    fl.nafn = nafn
    fl.stafir = stafir
    fl.url_vefs = url
    fl.save()

    print '%s (%s) is at %s (%s)' % (nafn, stafir, url,
                                     existing and 'updated' or 'new')

  def parse(self, url, data, fromEncoding=None):
    soup = ScraperParserHTML.parse(self, url, data.replace('"alt', '" alt'),
                                   fromEncoding=(fromEncoding or 'windows-1252'))
    urlbase, urldir = self.urls(url)

    for li in soup.fetch('li'):
      for a in li.fetch('a', {}, False):
        flokk_url = a.get('href', '')
        if flokk_url.startswith('/') and '/' not in flokk_url[1:]:
          stafir = flokk_url[1:]
          flokk_url = urlbase + stafir
          try:
            nafn = a.string
            self.skilgreina_flokk(nafn, stafir, flokk_url)
          except:
            traceback.print_exc()

    for tr in soup.fetch('tr'):
      for td in tr.fetch('td', {}, False):
        for a in td.fetch('a', {}, False):
          flokk_url = a.get('href', '')
          if 'thingfl=' in flokk_url:
            try:
              stafir = a.string
              nafn = tr.fetch('span', {'class': 'FyrirsognSv'})[0].string
              self.skilgreina_flokk(nafn, stafir, flokk_url)
            except:
              traceback.print_exc()

    return True

RegisterScraperParser(ScraperParserFlokkar)
RegisterBootstrap(FLOKKAR_URL)
