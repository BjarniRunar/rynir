import re
import traceback

from base import ScraperParser


SCRAPER_PARSERS = { }
BOOTSTRAP_URLS = [ ]

def RegisterScraperParser(cls):
  for rxp in cls.MATCH_URLS:
    SCRAPER_PARSERS[re.compile(rxp)] = cls

def RegisterBootstrap(url):
  BOOTSTRAP_URLS.append(url)


class MetaParser(ScraperParser):

  def _scrape_and_parse(self, url):
    scrape_id, data = self.scrape(url)
    if scrape_id and data is not None:
      return self.parse(url, data)
    else:
      return None

  scrape_and_parse = _scrape_and_parse

  def parse(self, url, data, fromEncoding=None):
    rv = None
    for rxp, cls in SCRAPER_PARSERS.iteritems():
      if rxp.match(url):
        #print 'Routing %s to %s' % (url, cls)
        sp = cls()
        sp.scrape_and_parse = self.scrape_and_parse
        try:
          rv = sp.parse(url, data, fromEncoding=fromEncoding
                        ) and (rv is None and True or rv)
        except:
          traceback.print_exc()
          rv = False
    if not rv:
      print 'No route for %s' % url
    return rv

  def bootstrap(self):
    for url in BOOTSTRAP_URLS:
      self.scrape_and_parse(url)
