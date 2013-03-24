import re
import traceback

from althingi.models import *
from htmlparser import ScraperParserHTML
from metaparser import RegisterScraperParser, RegisterBootstrap


def reify(url):
  return url.replace('.', '\\.').replace('?', '\\?').replace('[', '\\[') + '$'

THINGM_URL = ('http://www.althingi.is/dba-bin/thmn.pl?lthing=.&tegund=%DE&nuvam=1',
              'http://www.althingi.is/dba-bin/thmn.pl?lthing=.&tegund=[V]&radsv=U')
THINGM_RXP = (reify(THINGM_URL[0]), reify(THINGM_URL[1]))
MYND_URL = 'http://www.althingi.is/myndir/thingmenn-cache/%(nr)s/%(nr)s-220.jpg'

SKAMMSTOFUN_RE = re.compile('\\(([^)]+)\\)')


class ScraperParserThingmenn(ScraperParserHTML):
  MATCH_URLS = (THINGM_RXP[0], THINGM_RXP[1], )
  SCRAPE_URLS = ( )

  def parse(self, url, data, fromEncoding=None):
    soup = ScraperParserHTML.parse(self, url, data,
                                   fromEncoding=(fromEncoding or 'windows-1252'))
    urlbase, urldir = self.urls(url)

    # <tr><td ...><nobr><a href="/altext/cv.php4?...">Ossur ...</a> (OS)
    for tr in soup.fetch('tr'):
      for td in tr.fetch('td', {}, False):
        for nobr in td.fetch('nobr', {}, False):
          for a in nobr.fetch('a'):
            cv_url = a.get('href', '')
            if cv_url.startswith('/altext/cv.php4'):
              try:
                nr = cv_url.rsplit('=', 1)[1]
                nafn = a.string
                stafir = SKAMMSTOFUN_RE.search(unicode(nobr)).group(1)

                existing = Thingmadur.objects.filter(stafir=stafir)
                if existing:
                  thm = existing[0]
                else:
                  thm = Thingmadur()
                
                thm.nafn = nafn
                thm.stafir = stafir
                thm.url_vefs = urlbase + cv_url[1:]
                thm.url_mynd = MYND_URL % {'nr': nr}
                thm.save()
                print '%s is %s' % (stafir, nafn)
              except:
                traceback.print_exc()

    return True

RegisterScraperParser(ScraperParserThingmenn)
for url in THINGM_URL:
  RegisterBootstrap(url)
